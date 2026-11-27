# [Professor Dev] Forms for bugs, assignments and grading submissions
from django import forms
from django.db.models import Q
from pathlib import PurePosixPath
import re
from zipfile import BadZipFile, ZipFile

from core.models import AgentCredential, Assignment, Bug, StudyGroup
from core.projects import ProjectError, validate_project

LANGUAGES = [("python", "Python 3"), ("javascript", "JavaScript / Node.js")]


def accessible_bugs(user):
    return Bug.objects.filter(Q(created_by=user) | Q(visibility=Bug.Visibility.PUBLIC))


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ("bug", "title", "instructions", "deadline")
        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 3}),
            "deadline": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"},
            ),
        }
        help_texts = {"deadline": "Optional. Time zone: UTC. Results are visible after this time."}

    def __init__(self, *args, professor, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bug"].queryset = accessible_bugs(professor).order_by("title")


class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ("deadline",)
        widgets = {
            "deadline": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"},
            ),
        }


class ExerciseForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGES)
    project = forms.FileField(
        required=True, help_text="ZIP of the project folder. Text files only, up to 5 MB and 100 files.",
        widget=forms.ClearableFileInput(attrs={"accept": ".zip,application/zip"}),
    )
    entry_file = forms.CharField(required=False, help_text="Optional when there is one source file or a main.py/main.js. Otherwise enter its path inside the ZIP.")
    dockerfile = forms.FileField(required=False, label="Dockerfile (optional)",
                                help_text="Dockerfile as UTF-8 text, up to 50 KB. Stored with the project; automatic image builds are not enabled.")

    class Meta:
        model = Bug
        fields = ("title", "description", "language", "difficulty")
        labels = {"description": "Description (optional)", "difficulty": "Difficulty (optional)"}
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_project(self):
        upload = self.cleaned_data["project"]
        if not upload.name.lower().endswith(".zip"):
            raise forms.ValidationError("Choose a .zip project archive.")
        if upload.size > 5_000_000:
            raise forms.ValidationError("The ZIP exceeds 5 MB.")
        files = {}
        try:
            with ZipFile(upload) as archive:
                entries = archive.infolist()
                if len(entries) > 100 or sum(info.file_size for info in entries) > 5_000_000:
                    raise forms.ValidationError("Use at most 100 files and 5 MB of expanded content.")
                for info in entries:
                    path = PurePosixPath(info.filename)
                    if (
                        path.is_absolute() or ".." in path.parts or "\\" in info.filename
                        or ":" in info.filename
                        or ((info.external_attr >> 16) & 0o170000) == 0o120000
                    ):
                        raise forms.ValidationError("Use relative paths and regular files in the ZIP.")
                    if info.is_dir():
                        continue
                    name = str(path)
                    if name in files:
                        raise forms.ValidationError("The ZIP contains duplicate file paths.")
                    if any(part in (".git", ".env", "__pycache__", "node_modules") for part in path.parts):
                        raise forms.ValidationError("Remove secrets, Git data and generated dependencies from the ZIP.")
                    files[name] = archive.read(info).decode("utf-8")
        except (BadZipFile, UnicodeError, RuntimeError, NotImplementedError, OSError):
            raise forms.ValidationError("Upload a valid ZIP containing UTF-8 text files.")
        if not files:
            raise forms.ValidationError("The project is empty.")
        return files

    def clean_dockerfile(self):
        upload = self.cleaned_data.get("dockerfile")
        if not upload:
            return ""
        name = PurePosixPath(upload.name).name.lower()
        if upload.size > 50_000 or not (name == "dockerfile" or name.startswith("dockerfile.") or name.endswith(".dockerfile")):
            raise forms.ValidationError("Use Dockerfile, Dockerfile.<name> or a .dockerfile file up to 50 KB.")
        try:
            content = upload.read().decode("utf-8-sig")
        except UnicodeError:
            raise forms.ValidationError("Use UTF-8 text.")
        if "\x00" in content or not re.search(r"^\s*FROM\s+\S+", content, re.MULTILINE | re.IGNORECASE):
            raise forms.ValidationError("Upload a Dockerfile containing a FROM instruction.")
        return content

    def clean(self):
        data = super().clean()
        files = data.get("project")
        if files and not data.get("entry_file"):
            extension = ".py" if data.get("language") == "python" else ".js"
            preferred = "main" + extension
            candidates = [name for name in files if name.endswith(extension)
                          and not PurePosixPath(name).name.startswith("test")
                          and not name.endswith((".test.js", ".spec.js"))
                          and not any(part in ("tests", "test") for part in PurePosixPath(name).parts)]
            if preferred in files:
                data["entry_file"] = preferred
            elif len(candidates) == 1:
                data["entry_file"] = candidates[0]
        if not data.get("difficulty"):
            data["difficulty"] = Bug.Difficulty.EASY
        if files is not None and data.get("entry_file") not in files:
            self.add_error("entry_file", "Choose a file that exists in the uploaded project.")
        elif files is not None:
            try:
                validate_project(files, data["entry_file"])
            except ProjectError as error:
                self.add_error("project", str(error))
        return data


class GenerateForm(forms.Form):
    prompt = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={"rows": 5}))
    language = forms.ChoiceField(choices=LANGUAGES)
    test_count = forms.IntegerField(min_value=1, max_value=30, initial=5)


class KeyForm(forms.Form):
    provider = forms.ChoiceField(choices=AgentCredential.Provider.choices)
    key = forms.CharField(
        required=False, max_length=512, strip=True,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Save a new key to replace yours. Save an empty field to use the platform default.",
    )


class ExerciseDetailsForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ("title", "description", "difficulty")
        labels = {"description": "Description (optional)", "difficulty": "Difficulty (optional)"}
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class CatalogAssignmentForm(forms.Form):
    group = forms.ModelChoiceField(queryset=StudyGroup.objects.none())
    deadline = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    def __init__(self, *args, professor, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = StudyGroup.objects.filter(professor=professor)
