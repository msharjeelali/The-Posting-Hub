from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text="Please enter your date of birth"
    )
    
    class Meta:
        model = User
        fields = ('email', 'name', 'date_of_birth', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Remove username field
        if 'username' in self.fields:
            del self.fields['username']
        
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Add help text for password fields
        self.fields['password1'].help_text = "Your password must contain at least 8 characters."
        self.fields['password2'].help_text = "Enter the same password as before, for verification."
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("This email address is already in use. Please use a different email or try to login."))
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Generate a username from the email
        user.username = self.cleaned_data['email']
        # Split the name into first_name and last_name
        name_parts = self.cleaned_data['name'].split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': True})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(_("No account found with this email address."))
        return user.username 