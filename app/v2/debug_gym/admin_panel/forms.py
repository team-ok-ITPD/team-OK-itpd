# [Admin Dev] Forms for administrator-managed teacher accounts and memberships
from django import forms

from core.models import GroupStudent, User


class TeacherForm(forms.ModelForm):
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
        self.fields["name"].widget.attrs["placeholder"] = "Teacher's full name"
        self.fields["email"].widget.attrs.update(
            {"autocomplete": "email", "placeholder": "teacher@university.edu"}
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

    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.role = User.Role.PROFESSOR
        if self.cleaned_data.get("password"):
            teacher.set_password(self.cleaned_data["password"])
        if commit:
            teacher.save()
        return teacher


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
