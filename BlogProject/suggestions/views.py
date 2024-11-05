from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from posts.models import Post

from .models import Suggestion, SuggestionReply


# Create your views here.
@login_required
def user_suggestions(request):
    if request.method == "POST":
        suggestion_id = request.POST.get("suggestion_id")
        action = request.POST.get("action")

        # Get the suggestion object
        try:
            suggestion = Suggestion.objects.get(id=suggestion_id)
            if action == "accept":
                suggestion.status = "accepted"
                # print status
                print(
                    f"Suggestion {suggestion_id} updated to {
                        suggestion.status}")
                suggestion.save()
            elif action == "reject":
                suggestion.status = "rejected"
                suggestion.save()

        except Suggestion.DoesNotExist:
            pass

        # Redirect to the same page to reflect the updated status
        return redirect("suggestions:user_suggestions")

    user_posts = Post.objects.filter(author=request.user)
    suggestions = Suggestion.objects.filter(post__in=user_posts)

    context = {
        "suggestions": suggestions,
    }

    return render(
        request,
        "suggestions/user_suggestions_content.html",
        context)


@login_required
def submit_reply(request):
    if request.method == "POST":
        suggestion_id = request.POST.get("suggestion_id")
        reply_content = request.POST.get("reply_content")

        suggestion = get_object_or_404(Suggestion, id=suggestion_id)

        if suggestion.reply:
            # If a reply already exists, you might want to update it or prevent double submissions.
            # Here, we will update the existing reply.
            suggestion.reply.content = reply_content
            suggestion.reply.save()
        else:
            # Create a new reply and associate it with the suggestion
            reply = SuggestionReply.objects.create(
                user=request.user, content=reply_content
            )
            suggestion.reply = reply
            suggestion.save()

        return redirect(
            "suggestions:user_suggestions"
        )  # Redirect to the user suggestions page or another page

    return redirect("suggestions:user_suggestions")


@login_required
def user_submitted_suggestions(request):
    suggestions = Suggestion.objects.filter(user=request.user)

    context = {"suggestions": suggestions}
    return render(
        request,
        "suggestions/user_submitted_suggestions.html",
        context)
