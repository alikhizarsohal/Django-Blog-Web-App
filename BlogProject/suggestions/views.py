from django.shortcuts import redirect, render

from posts.models import Post
from .models import Suggestion

# Create your views here.
# @login_required
def user_suggestions(request):
    if request.method == 'POST':
        suggestion_id = request.POST.get('suggestion_id')
        action = request.POST.get('action')
        
        # Get the suggestion object
        try:
            suggestion = Suggestion.objects.get(id=suggestion_id)
            if action == 'accept':
                suggestion.status = 'accepted'
                # print status
                print(f'Suggestion {suggestion_id} updated to {suggestion.status}')
                suggestion.save()
            elif action == 'reject':
                suggestion.delete()

        except Suggestion.DoesNotExist:
            pass
        
        # Redirect to the same page to reflect the updated status
        return redirect('suggestions:user_suggestions')
    
    user_posts = Post.objects.filter(author=request.user)
    suggestions = Suggestion.objects.filter(post__in=user_posts)

    context = {
        'suggestions': suggestions,
    }

    return render(request, 'suggestions/user_suggestions_content.html', context)