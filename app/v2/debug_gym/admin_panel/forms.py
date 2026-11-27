# [Admin Dev] Forms for administrator-managed teacher accounts and memberships
from django import forms
from django.conf import settings

from core.models import StudyGroup, User


class VisiblePasswordInput(forms.PasswordInput):
    # Reveal only new input, without redisplaying submitted values or stored hashes.
    input_type = "text"


class TeacherForm(forms.ModelForm):
    account_role = User.Role.PROFESSOR
    password = forms.CharField(
        label="New password",
        min_length=8,
        required=False,
        strip=False,
        help_text="At least 8 characters. Leave blank to keep the current password.",
        widget=VisiblePasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        model = User
        fields = ["name", "email", "is_active"]

    def __init__(self, *args, creating=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "Full name"
        self.fields["email"].widget.attrs.update(
            {"autocomplete": "email", "placeholder": "name@university.edu"}
        )
        if creating:
            self.fields["password"].label = "Password"
            self.fields["password"].required = not settings.ACCOUNT_EMAIL_ENABLED
            self.fields["password"].help_text = (
                "At least 8 characters. When email is enabled, the initial password "
                "and a setup link are emailed. Without a password, only the link is sent."
            )

    def clean_email(self):
        email = User.objects.normalize_email(self.cleaned_data["email"].strip())
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.role = self.account_role
        if self.cleaned_data.get("password"):
            teacher.set_password(self.cleaned_data["password"])
        elif not teacher.pk:
            teacher.set_unusable_password()
        if commit:
            teacher.save()
        return teacher


class StudentForm(TeacherForm):
    account_role = User.Role.STUDENT


class AdministratorForm(TeacherForm):
    account_role = User.Role.ADMIN


class GroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ["name", "course", "group_number", "description", "professor"]
        labels = {
            "name": "Group name", "course": "Course", "group_number": "Group number", "professor": "Teacher",
        }
        help_texts = {
            "description": "Optional notes about the group.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "e.g. Programming"
        self.fields["group_number"].required = True
        self.fields["group_number"].widget.attrs["placeholder"] = "e.g. 01 or BS-23"
        self.fields["professor"].queryset = User.objects.filter(
            role=User.Role.PROFESSOR, is_active=True
        )
        if self.instance.pk:
            self.fields["professor"].empty_label = None
        self.fields["professor"].widget.attrs["data-searchable-select"] = "Search teachers"

    def clean(self):
        data = super().clean()
        if data.get("name") and data.get("group_number"):
            if StudyGroup.objects.filter(
                name__iexact=data["name"], group_number__iexact=data["group_number"]
            ).exclude(pk=self.instance.pk).exists():
                self.add_error("group_number", "This group number already exists for this course.")
        return data


class StudentBatchForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role=User.Role.STUDENT),
        widget=forms.MultipleHiddenInput,
    )
    action = forms.ChoiceField(choices=[
        ("add", "Add to group"), ("remove", "Remove from group"),
        ("activate", "Activate"), ("deactivate", "Deactivate"),
    ])
    group = forms.ModelChoiceField(
        queryset=StudyGroup.objects.all(), required=False, empty_label="",
        widget=forms.Select(attrs={
            "data-searchable-select": "Search target groups",
            "data-empty-placeholder": "",
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound and self.data.get("action") in ("activate", "deactivate"):
            # Status changes concern selected accounts, never group membership.
            self.fields["group"].disabled = True

    def clean(self):
        data = super().clean()
        if data.get("action") in ("add", "remove") and not data.get("group"):
            self.add_error("group", "Choose a group.")
        if data.get("action") == "add" and data.get("students") is not None:
            if data["students"].filter(is_active=False).exists():
                self.add_error("students", "Activate all selected students before enrollment.")
        return data


class StudentImportForm(forms.Form):
    file = forms.FileField(label="UTF-8 CSV file")
    confirm = forms.BooleanField(
        label="Apply account updates and add memberships from this file."
    )

    def clean_file(self):
        file = self.cleaned_data["file"]
        if file.size > 1_000_000:
            raise forms.ValidationError("The CSV must be at most 1 MB.")
        return file
