# [Student Dev] Forms for submitting bug fixes
from django import forms

from core.models import Bug

from .ai import PROVIDER_CHOICES
from .workspaces import bug_tests_code, build_project

MAX_CODE_LENGTH = 50_000
CODE_ATTRS = {"spellcheck": "false", "autocapitalize": "off", "rows": 10, "class": "code-input"}


def normalize_code(code):
    """Browsers send textarea newlines as CRLF; store and compare with LF only."""
    return code.replace("\r\n", "\n").replace("\r", "\n")


class SubmissionForm(forms.Form):
    code = forms.CharField(
        strip=False,  # keep indentation and trailing newlines exactly as typed
        max_length=MAX_CODE_LENGTH,
        widget=forms.Textarea(attrs={"spellcheck": "false", "autocapitalize": "off", "rows": 20}),
        error_messages={"required": "Your fix is empty. Write some code before submitting."},
    )

    def __init__(self, *args, bug, **kwargs):
        self.bug = bug
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = normalize_code(self.cleaned_data["code"])
        if not code.strip():
            raise forms.ValidationError("Your fix is empty. Write some code before submitting.")
        if code.strip() == normalize_code(self.bug.buggy_code).strip():
            raise forms.ValidationError(
                "This is still the original buggy code. Change something before submitting."
            )
        return code


class StudentBugForm(forms.ModelForm):
    """Edit a student's own practice bug (created_by is set by the view).

    The code and tests are stored in the bug's project files (core.projects), the
    same place the professor pages and server-side verification read them from.
    """

    # Not a model field: saved as test_main.py in the bug's project files.
    tests_code = forms.CharField(
        label="Tests (optional, Python only)",
        required=False,
        strip=False,
        widget=forms.Textarea(attrs=CODE_ATTRS),
        help_text="A pytest file. The code is saved as main.py, so start with: from main import *",
    )

    class Meta:
        model = Bug
        fields = ["title", "description", "language", "difficulty", "visibility", "buggy_code", "tests_code"]
        labels = {
            "buggy_code": "Buggy code",
            "visibility": "Who can practise it",
        }
        help_texts = {
            "description": "What should the code do, and what goes wrong?",
            "language": "",  # the placeholder already gives examples
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "language": forms.TextInput(attrs={"list": "language-options", "placeholder": "e.g. python"}),
            "visibility": forms.RadioSelect,
            "buggy_code": forms.Textarea(attrs=CODE_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep code exactly as typed: stripping would remove the first line's indentation.
        for name in ("buggy_code", "tests_code"):
            self.fields[name].strip = False
        self.fields["visibility"].choices = [
            (Bug.Visibility.PRIVATE, "Only me"),
            (Bug.Visibility.PUBLIC, "Every student"),
        ]
        if not self.instance.pk:
            self.initial.setdefault("visibility", Bug.Visibility.PRIVATE)
        else:
            self.initial.setdefault("tests_code", bug_tests_code(self.instance))

    def clean_language(self):
        return self.cleaned_data["language"].strip().lower()

    def clean_buggy_code(self):
        code = normalize_code(self.cleaned_data["buggy_code"])
        if not code.strip():
            raise forms.ValidationError("Add the buggy code to practise on.")
        return code

    def clean_tests_code(self):
        return normalize_code(self.cleaned_data.get("tests_code") or "")

    def save(self, commit=True):
        bug = super().save(commit=False)
        bug.project_files, bug.entry_file = build_project(
            bug.language, bug.buggy_code, self.cleaned_data["tests_code"], base=bug.project_files,
        )
        if bug.pk:
            bug.revision += 1  # open VS Code folders and running checks see the change
        if commit:
            bug.save()
        return bug


class AIBugForm(forms.Form):
    """Ask an AI to write a practice bug. The API key is used once and never saved."""

    provider = forms.ChoiceField(label="AI provider", choices=PROVIDER_CHOICES)
    api_key = forms.CharField(
        label="API key",
        strip=True,
        widget=forms.PasswordInput(attrs={"autocomplete": "off", "spellcheck": "false"}),
        help_text="Your own key for the provider above. It is used for this request only and never saved.",
    )
    model = forms.CharField(
        label="Model (optional)",
        required=False,
        max_length=100,
        help_text="Leave empty to use the provider's default model.",
    )
    prompt = forms.CharField(
        label="What should the bug be about?",
        max_length=1000,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "e.g. a function that finds the second largest number in a list"}),
    )
    language = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"list": "language-options", "placeholder": "e.g. python"}),
    )
    difficulty = forms.ChoiceField(choices=Bug.Difficulty.choices, initial=Bug.Difficulty.EASY)
    visibility = forms.ChoiceField(
        label="Who can practise it",
        choices=[(Bug.Visibility.PRIVATE, "Only me"), (Bug.Visibility.PUBLIC, "Every student")],
        initial=Bug.Visibility.PRIVATE,
        widget=forms.RadioSelect,
    )

    def clean_language(self):
        return self.cleaned_data["language"].strip().lower()
