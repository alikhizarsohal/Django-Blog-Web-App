from django.shortcuts import get_object_or_404, redirect, render

from BlogApp.forms import CommentForm
from .models import Comment

# Create your views here.
# @login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('posts:post_detail', post_id=comment.post.id)

# @login_required
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
            return redirect('posts:post_detail', post_id=parent_comment.post.id)
    else:
        form = CommentForm()
    
    return render(request, 'comments/reply_to_comment.html', {'form': form, 'parent_comment': parent_comment})
