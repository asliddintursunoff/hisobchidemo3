from django import forms
import re
from .models import User

class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=13,  # +998XXXXXXXXX (13 chars)
        required=True,
        label="Phone Number",
        widget=forms.TextInput(attrs={"placeholder": "+998 XX XXX-XX-XX", "class": "form-control"})
    )

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not re.match(r"^\+998\d{9}$", phone):
            raise forms.ValidationError("Invalid Uzbek phone number format! It should be +998XXXXXXXXX.")
        return phone

    class Meta:
        model = User
        fields = ["phone_number"]
