from django import forms
from .models import Post, Comment
from core.models import UserProfile
# -----------------------------------------------------
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
# -----------------------------------------------------

User = get_user_model()

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'content']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
#             'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your post content here...'}),
#         }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your post content here...'
            })
        }


# -----------------------------------------------------
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
# -----------------------------------------------------

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for users or posts...'
        })
    ) 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'bio', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'dob-input'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
                'id': 'bio-textarea'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to all fields automatically
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here...'})
        }