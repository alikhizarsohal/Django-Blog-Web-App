from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from comments.models import Comment, CommentAttachment
from posts.models import Post, PostAttachment
from reports.models import Report
from suggestions.models import Suggestion

from .models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        error_messages={"required": "First name is required."},
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        error_messages={"required": "Last name is required."},
    )
    profile_picture = forms.ImageField(
        required=False, error_messages={"invalid": "Invalid image file."}
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "profile_picture",
        ]
        widgets = {
            "profile_picture": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={"autofocus": True}),
        error_messages={"required": "Username or email is required."},
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        error_messages={"required": "Password is required."},
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                # Add custom error message if authentication fails
                print("-----------------------------------------")
                self.add_error(
                    None, "Invalid username or password. Please check your credentials.")

        return cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("This account is inactive.")
        if not user.email_confirmed:
            raise ValidationError(
                "Email address must be confirmed before logging in.")


class PostForm(forms.ModelForm):
    attachment = forms.FileField(required=False)  # Single file upload field

    class Meta:
        model = Post
        fields = ["title", "content"]

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
        return post

    def save_attachment(self, post, file):
        if file:
            PostAttachment.objects.create(post=post, file=file)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class CommentAttachmentForm(forms.ModelForm):
    class Meta:
        model = CommentAttachment
        fields = ["file"]


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason"]


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ["content"]


class EditProfileForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(), required=False, label="New Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Confirm New Password")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_id = self.instance.id  # Get the ID of the current user instance
        if User.objects.filter(email=email).exclude(pk=user_id).exists():
            raise forms.ValidationError(
                "A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned_data
