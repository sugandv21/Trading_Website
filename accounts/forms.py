# accounts/forms.py
from django import forms
from .models import PartnerLead

class PartnerLeadForm(forms.ModelForm):
    class Meta:
        model = PartnerLead
        fields = ["name", "phone", "email", "city", "pincode"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control rounded-pill", "placeholder": "Your Name"}),
            "phone": forms.TextInput(attrs={"class": "form-control rounded-pill", "placeholder": "Phone Number"}),
            "email": forms.EmailInput(attrs={"class": "form-control rounded-pill", "placeholder": "E-Mail Id"}),
            "city": forms.TextInput(attrs={"class": "form-control rounded-pill", "placeholder": "City"}),
            "pincode": forms.TextInput(attrs={"class": "form-control rounded-pill", "placeholder": "Pin Code"}),
        }

class VerifyOtpForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={"class": "form-control rounded-pill", "placeholder": "Enter OTP"})
    )
