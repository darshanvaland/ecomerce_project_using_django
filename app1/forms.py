from django import forms
from app1.models import Register,feedback


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model=Register
        fields='__all__'

class UserfeedbackForm(forms.ModelForm):
    class Meta:
        model=feedback
        fields='__all__'
