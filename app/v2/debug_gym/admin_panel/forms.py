# [Admin Dev] Forms for administrator-managed teacher accounts and memberships
from django import forms
from django.db.models import Q

from core.models import StudyGroup, User


class MembershipChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, group):
        status = " · Inactive" if not group.is_active else ""
        return f"{group} · {group.course or 'No course'} · {group.professor.name}{status}"


class TeacherForm(forms.ModelForm):
    account_role = User.Role.PROFESSOR

    class Meta:
        model = User
        fields = ["name", "email", "is_active"]

    def __init__(self, *args, creating=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "Full name"
        self.fields["email"].widget.attrs.update(
            {"autocomplete": "email", "placeholder": "name@university.edu"}
        )

    def clean_email(self):
        email = User.objects.normalize_email(self.cleaned_data["email"].strip())
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.role = self.account_role
        if not teacher.pk:
            teacher.set_unusable_password()
        if commit:
            teacher.save()
        return teacher


class StudentForm(TeacherForm):
    account_role = User.Role.STUDENT
    groups = MembershipChoiceField(
        queryset=StudyGroup.objects.select_related("professor").order_by("-is_active", "name", "pk"), required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Membership is independent of account activity. Inactive groups retain their materials.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["groups"].initial = self.instance.study_groups.values_list("pk", flat=True)

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.study_groups.set(self.cleaned_data["groups"])
        return user


class AdministratorForm(TeacherForm):
    account_role = User.Role.ADMIN


class GroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ["name", "course", "description", "professor", "is_active"]
        labels = {
            "name": "Group name", "course": "Course", "professor": "Teacher", "is_active": "Active group",
        }
        help_texts = {
            "description": "Optional notes about the group.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "e.g. Programming"
        self.fields["is_active"].help_text = (
            "Deactivation keeps membership, assignments and student access. Inactive groups appear last."
        )
        self.fields["professor"].queryset = User.objects.filter(
            Q(is_active=True) | Q(pk=self.instance.professor_id),
            role=User.Role.PROFESSOR,
        )
        if self.instance.pk:
            self.fields["professor"].empty_label = None
        self.fields["professor"].widget.attrs["data-searchable-select"] = "Search teachers"

    def clean(self):
        data = super().clean()
        if data.get("name"):
            if StudyGroup.objects.filter(
                name__iexact=data["name"],
            ).exclude(pk=self.instance.pk).exists():
                self.add_error("name", "A group with this name already exists.")
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
