from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import CommentAttachment, User, Post, Comment, Report, Suggestion
from .forms import CommentAttachmentForm, CommentForm, ReportForm, SuggestionForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import CustomUserCreationForm
from .forms import PostForm

from django.utils import timezone
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Include request.FILES for profile_picture
        if form.is_valid():
            user = form.save()
            user.is_active = True  # Activate account immediately
            user.save()
            
            return redirect('login')  # Redirect to login page after registration
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})



def login(request):
    print("Entered login view")

    if request.method == 'POST':
        print("Processing POST request")
        form = CustomAuthenticationForm(data=request.POST)
        print("Form created")

        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(username=username)
                print(f"User found: {username}")

                if user.lockout_until and user.lockout_until > timezone.now():
                    print("Account is locked")
                    form.add_error(None, 'Account locked. Try again later.')
                else:
                    user_auth = authenticate(request, username=username, password=password)
                    print(f"Authenticate result: {user_auth}")

                    if user_auth is not None:
                        if user_auth == user:
                            print("User authenticated successfully")
                            auth_login(request, user_auth)
                            user.reset_failed_login_attempts()
                            return redirect('dashboard')
                        else:
                            print("Invalid password")
                            user.increment_failed_login_attempts()
                            form.add_error(None, 'Invalid username or password. Please check your credentials.')
                    else:
                        print("Authentication failed")
                        user.increment_failed_login_attempts()
                        form.add_error(None, 'Invalid username or password. Please check your credentials.')

            except User.DoesNotExist:
                print("User does not exist")
                form.add_error(None, 'Invalid username or password. Please check your credentials.')

        else:
            print("Form errors:", form.errors)

    else:
        print("GET request")
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to login page after logging out

@login_required
def dashboard(request):
    user = request.user  # Get the current logged-in user
    recent_comments_on_posts = Comment.objects.filter(
        post__in=user.posts.all()
    ).order_by('-created_at')[:5]


    # Count the total posts made by the user
    posts_count = user.posts.count()

    # Get the most recent post made by the user
    recent_posts = user.posts.order_by('-created_at')[:5]  # Get the 5 most recent posts

    # Get the most recent likes made by the user from the post table as there is no like table
     # Fetch recent likes for the posts

    posts = Post.objects.prefetch_related('likes').all()
    # Create a list of posts with their likes

    context = {
        'user': user,
        'recent_comments_on_posts': recent_comments_on_posts,
        'posts_count': posts_count,
        'recent_posts': recent_posts,
        'posts': posts
    }
    return render(request, 'blog/dashboard.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Handle single file upload
            file = request.FILES.get('attachment')
            form.save_attachment(post, file)

            return redirect('dashboard')  # Adjust as needed
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent_comment__isnull=True)

    if request.method == 'POST':
        # Handle comment submission with attachments
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                # Handle attachments
                attachment_form = CommentAttachmentForm(request.POST, request.FILES)
                if attachment_form.is_valid():
                    for attachment in request.FILES.getlist('file'):
                        CommentAttachment.objects.create(comment=comment, file=attachment)

                return redirect('post_detail', post_id=post.id)

        # Handle report submission
        if 'submit_report' in request.POST:
            report_form = ReportForm(request.POST)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.post = post
                report.reported_by = request.user
                report.save()
                return redirect('post_detail', post_id=post.id)

        # Handle suggestion submission
        if 'submit_suggestion' in request.POST:
            suggestion_form = SuggestionForm(request.POST)
            if suggestion_form.is_valid():
                suggestion = suggestion_form.save(commit=False)
                suggestion.post = post
                suggestion.user = request.user
                suggestion.save()
                return redirect('post_detail', post_id=post.id)

    else:
        comment_form = CommentForm()
        attachment_form = CommentAttachmentForm()  # Initialize an empty form for attachments
        report_form = ReportForm()
        suggestion_form = SuggestionForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'attachment_form': attachment_form,
        'report_form': report_form,
        'suggestion_form': suggestion_form,
    }

    return render(request, 'blog/post_detail.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post.id)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('post_detail', post_id=comment.post.id)

@login_required
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = parent_comment.post
            reply.author = request.user
            reply.parent_comment = parent_comment
            reply.save()
            return redirect('post_detail', post_id=parent_comment.post.id)
    else:
        form = CommentForm()
    
    return render(request, 'blog/reply_to_comment.html', {'form': form, 'parent_comment': parent_comment})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.author = request.user
            comment.save()

            # Handle attachments
            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                CommentAttachment.objects.create(comment=comment, file=attachment)

            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form})

@login_required
def report_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        reason = request.POST.get('reason')
        
        Report.objects.create(
            report_type='post',
            post=post,
            reported_by=request.user,
            reason=reason
        )
        
        return redirect('post_detail', post_id=post_id)

@login_required
def report_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        reason = request.POST.get('reason')
        
        # Create the report
        Report.objects.create(
            report_type='comment',
            comment=comment,
            reported_by=request.user,
            reason=reason
        )
        
        # Redirect to the referring page if it exists
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        
        # Fallback redirect if referer is not available
        return redirect('blog/post_detail')  # Change 'home' to a valid URL or view name
    
    return HttpResponseBadRequest("Invalid request method.")

@login_required
def suggest_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        
        # Simplified debugging
        print("Request POST data:", request.POST)
        print("Content from request.POST:", content)

        if content:
            Suggestion.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            print("No content provided")
    
 
    return redirect('blog/post_detail')  # Fallback redirect if the request method is not POST

@login_required
def post_list(request):
    posts = Post.objects.all()  # Fetch all posts
    return render(request, 'blog/post_list.html', {'posts': posts})


