# [Admin Dev] Forms for administrator-managed teacher accounts and memberships
from django import forms

from core.models import GroupStudent, StudyGroup, User


class TeacherForm(forms.ModelForm):
    account_role = User.Role.PROFESSOR
    password = forms.CharField(
        min_length=8,
        required=False,
        strip=False,
        help_text="At least 8 characters. Leave blank to keep the current password.",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password_confirmation = forms.CharField(
        required=False,
        strip=False,
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
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
            self.fields["password"].required = True
            self.fields["password_confirmation"].required = True
            self.fields["password"].help_text = "At least 8 characters."

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirmation"):
            self.add_error("password_confirmation", "Passwords do not match.")
        return cleaned_data

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
        fields = ["name", "description", "professor"]
        labels = {"professor": "Teacher"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["professor"].queryset = User.objects.filter(
            role=User.Role.PROFESSOR, is_active=True
        )


class GroupMemberForm(forms.Form):
    student = forms.ModelChoiceField(queryset=User.objects.none())

    def __init__(self, *args, group, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group
        self.fields["student"].queryset = User.objects.filter(
            role=User.Role.STUDENT,
            is_active=True,
        ).exclude(groupstudent__group=group)

    def clean_student(self):
        student = self.cleaned_data["student"]
        if student.role != User.Role.STUDENT:
            raise forms.ValidationError("Only student accounts can join a teaching group.")
        if GroupStudent.objects.filter(group=self.group, student=student).exists():
            raise forms.ValidationError("This student is already in the group.")
        return student
