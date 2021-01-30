from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["password"].widget.input_type = "password"
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password"
        ]