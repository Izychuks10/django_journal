# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Journal, Blog  # Import the Journal and Blog models
from .models import TeamMember
from .models import Comment


class JournalForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea, label='Content')

    class Meta:
        model = Journal  # Ensure you have a Journal model defined
        fields = ['title', 'content']

class BlogForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea, label='Content')

    class Meta:
        model = Blog  # Ensure you have a Blog model defined
        fields = ['title', 'content']
        

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']
        # Set help_texts to empty strings to hide them
        help_texts = {
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        # Check for existing username and email
        if User.objects.filter(username=username).exists():
            self.add_error('username', "Username already exists.")
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Email already exists.")

        # Check if passwords match
        if password != password2:
            self.add_error('password2', "Passwords do not match.")



class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'position', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }