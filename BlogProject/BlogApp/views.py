from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.timezone import now
from pyexpat.errors import messages

from comments.models import Comment, CommentAttachment
from posts.models import Post
from reports.models import Report
from suggestions.models import Suggestion, SuggestionReply

from .forms import (CommentAttachmentForm, CommentForm,
                    CustomAuthenticationForm, CustomUserCreationForm,
                    EditProfileForm, PostForm, ReportForm, SuggestionForm)
from .models import User


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(
            request.POST, request.FILES
        )  # Include request.FILES for profile_picture
        if form.is_valid():
            user = form.save()
            user.is_active = True  # Activate account immediately
            user.save()
            send_confirmation_email(user, request)
            # Redirect to login page after registration
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


def send_confirmation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    email_subject = "Confirm your email address"
    email_body = render_to_string(
        "email/confirm_email.html",
        {
            "user": user,
            "uid": uid,
            "token": token,
            "protocol": "https" if request.is_secure() else "http",
            "domain": request.get_host(),
        },
    )
    send_mail(email_subject,
              email_body,
              settings.DEFAULT_FROM_EMAIL,
              [user.email])
    user.confirmation_sent_at = now()
    user.save()


def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_confirmed = True
        user.is_active = True
        user.save()
        auth_login(request, user)
        return redirect("dashboard")
    else:
        return render(request, "register/invalid_link.html")


def login(request):
    print("Entered login view")

    if request.method == "POST":
        print("Processing POST request")
        form = CustomAuthenticationForm(data=request.POST)
        print("Form created")

        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            try:
                user = User.objects.get(username=username)
                print(f"User found: {username}")

                if user.lockout_until and user.lockout_until > timezone.now():
                    print("Account is locked")
                    form.add_error(None, "Account locked. Try again later.")
                else:
                    user_auth = authenticate(
                        request, username=username, password=password
                    )
                    print(f"Authenticate result: {user_auth}")

                    if user_auth is not None:
                        if user_auth == user:
                            print("User authenticated successfully")
                            auth_login(request, user_auth)
                            user.reset_failed_login_attempts()
                            return redirect("dashboard")
                        else:
                            print("Invalid password")
                            user.increment_failed_login_attempts()
                            form.add_error(
                                None, "Invalid username or password. Please check your credentials.", )
                    else:
                        print("Authentication failed")
                        user.increment_failed_login_attempts()
                        form.add_error(
                            None, "Invalid username or password. Please check your credentials.", )

            except User.DoesNotExist:
                print("User does not exist")
                form.add_error(
                    None, "Invalid username or password. Please check your credentials.")

        else:
            print("Form errors:", form.errors)

    else:
        print("GET request")
        form = CustomAuthenticationForm()

    return render(request, "login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("login")  # Redirect to login page after logging out


@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            old_email = user.email
            new_email = form.cleaned_data.get("email")

            # Check if the email was changed
            if old_email != new_email:
                # Check if the new email already exists in the database
                # excluding the current user
                if User.objects.filter(
                        email=new_email).exclude(
                        pk=user.pk).exists():
                    messages.error(
                        request, "A user with this email already exists.")
                    return redirect("edit_profile")
                else:
                    user.email_confirmed = False
                    user.confirmation_sent_at = timezone.now()
                    send_confirmation_email(
                        user, request
                    )  # Assuming this function sends an email confirmation

            # Save the user's changes
            user = form.save(commit=False)

            # Check if the user updated their password
            if form.cleaned_data.get("password1"):
                user.set_password(form.cleaned_data.get("password1"))

            user.save()

            # Optionally, update the session authentication hash to keep the user logged in after a password change
            # update_session_auth_hash(request, user)

            return redirect("login")
        else:
            # This will print out the form errors in the terminal
            print(form.errors)

    else:
        form = EditProfileForm(instance=user)

    return render(request, "edit_profile.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user  # Get the current logged-in user

    # Fetch recent comments on posts created by the user
    recent_comments_on_posts = Comment.objects.filter(
        post__in=user.posts.all()
    ).order_by("-created_at")[:5]

    # Count the total posts made by the user
    posts_count = user.posts.count()

    # Get the most recent posts made by the user
    recent_posts = Post.objects.order_by("-created_at")[
        :5
    ]  # Get the 5 most recent posts

    # Get the most recent likes made by the user from the post table (assuming
    # a 'likes' field exists)
    posts = Post.objects.prefetch_related("likes").all()

    # Check if the user wants to see suggestions
    show_suggestions = request.GET.get("section") == "suggestions"

    # Fetch suggestions if the user wants to see them
    suggestions = []
    if show_suggestions:
        suggestions = Suggestion.objects.filter(post__author=user)

    context = {
        "user": user,
        "recent_comments_on_posts": recent_comments_on_posts,
        "posts_count": posts_count,
        "recent_posts": recent_posts,
        "posts": posts,
        "suggestions": suggestions,
        "show_suggestions": show_suggestions,
    }

    return render(request, "blog/dashboard.html", context)


@login_required
def report_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        reason = request.POST.get("reason")

        # Create the report
        Report.objects.create(
            report_type="comment",
            comment=comment,
            reported_by=request.user,
            reason=reason,
        )

        # Redirect to the referring page if it exists
        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)

        # Fallback redirect if referer is not available
        return redirect(
            "posts/post_detail"
        )  # Change 'home' to a valid URL or view name

    return HttpResponseBadRequest("Invalid request method.")


@login_required
def reply_to_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)

    if request.method == "POST":
        reply_content = request.POST.get("reply_content")

        if reply_content:
            # Create a reply to the suggestion
            reply = SuggestionReply.objects.create(
                suggestion=suggestion,
                user=request.user,  # Assuming this is the post author
                content=reply_content,
            )
            print("Suggestion reply created:", reply)

            # Associate the reply with the suggestion
            suggestion.reply = reply
            suggestion.save()

            return redirect(request.META.get("HTTP_REFERER", "home"))
        else:
            print("No reply content provided")
            # Optionally, add a message to the user indicating that the reply content is required
            # messages.error(request, "Content is required to submit a reply.")

    return redirect(
        "posts:post_detail", post_id=suggestion.post.id
    )  # Redirect to the post detail view


@login_required
def jump_to_suggestions(request):
    print("Jump to suggestions")
    return redirect("suggestions:user_suggestions")


@login_required
def jump_to_posts(request):
    print("Jump to posts")
    return redirect("posts:post_list")


# Utility function to check if the user is a moderator
def is_moderator(user):
    return user.is_authenticated and user.groups.filter(
        name="Moderators").exists()


# Moderator view to manage posts
@user_passes_test(is_moderator)
def moderator(request):
    # Retrieve all posts (you can filter them if needed)
    posts = Post.objects.all()

    # Render the template with the posts data
    return render(request, "moderator.html", {"posts": posts})

def base(request):
    return render(request, 'base.html')

def role_user(request):
    return render(request, 'login.html')

def role_admin(request):
    # Redirect to the Django admin portal
    return redirect('/admin/')

def role_moderator(request):
    # Redirect to the Django admin portal
    return redirect('/admin/')
