from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "name-field"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "id": "email-field"}),
            "subject": forms.TextInput(
                attrs={"class": "form-control", "id": "subject-field"}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "id": "message-field", "rows": 8}
            ),
        }
