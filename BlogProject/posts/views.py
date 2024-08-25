from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist

from BlogApp.forms import CommentAttachmentForm, CommentForm, PostForm, ReportForm, SuggestionForm

from comments.models import Comment, CommentAttachment
from reports.models import Report
from suggestions.models import Suggestion
from .models import Post, PostAttachment


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

    return render(request, 'posts/create_post.html', {'form': form})

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

                return redirect('posts:post_detail', post_id=post.id)

        # Handle report submission
        if 'submit_report' in request.POST:
            report_form = ReportForm(request.POST)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.post = post
                report.reported_by = request.user
                report.save()
                return redirect('posts:post_detail', post_id=post.id)

        # Handle suggestion submission
        if 'submit_suggestion' in request.POST:
            suggestion_form = SuggestionForm(request.POST)
            if suggestion_form.is_valid():
                suggestion = suggestion_form.save(commit=False)
                suggestion.post = post
                suggestion.user = request.user
                suggestion.save()
                return redirect('posts:post_detail', post_id=post.id)

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

    return render(request, 'posts/post_detail.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('posts:post_detail', post_id=post.id)


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

            return redirect('posts:post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'posts/add_comment.html', {'form': form})

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
        
        return redirect('posts:post_detail', post_id=post_id)

@login_required
def suggest_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        # Debugging output (optional)
        print("Request POST data:", request.POST)
        print("Content from request.POST:", content)

        if content:
            # Create a new suggestion
            suggestion = Suggestion.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            print("Suggestion created:", suggestion)
            
            return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect back to the previous page
        else:
            # Handle the case where no content was provided
            print("No content provided")
            # Optionally, add a message to the user indicating that the content is required
            # messages.error(request, "Content is required to submit a suggestion.")
    
    return redirect('posts:post_detail', post_id=post.id)  # Redirect to the post detail view if not POST

@login_required
def post_list(request):
    # Get search parameters
    author_query = request.GET.get('author', '')
    title_query = request.GET.get('title', '')
    date_published_query = request.GET.get('date_published', '')
    posts = Post.objects.filter(is_published=True)  # Fetch only published posts 
    
    if author_query:
        posts = posts.filter(author__username__icontains=author_query)
    if title_query:
        posts = posts.filter(title__icontains=title_query)
    if date_published_query:
        posts = posts.filter(created_at__date=date_published_query)

    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def my_post_list(request):
    posts = Post.objects.filter(author=request.user)  # Fetch posts authored by the logged-in user
    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def edit_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id, author=request.user)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:post_detail', post_id=post.id)
        else:
            form = PostForm(instance=post)

        context = {
            'form': form,
            'post': post,
        }

        return render(request, 'posts/edit_post.html', context)
    except TemplateDoesNotExist:
        return HttpResponseServerError("Template not found.")