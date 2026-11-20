# [Student Dev] Forms for submitting bug fixes
from django import forms

MAX_CODE_LENGTH = 50_000


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
