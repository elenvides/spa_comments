from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CommentsListView(ListView):
    model = Comment
    template_name = 'comments/comments_list.html'
    context_object_name = 'comments'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user

            parent_comment_id = request.POST.get('parent_comment')

            if parent_comment_id:
                form.instance.parent_comment = Comment.objects.get(id=parent_comment_id)
            form.save()
            return redirect('comments_list')
        else:
            return self.get(request, form=form)

    def get(self, request, *args, form=None, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(form=form if form else CommentForm())
        return self.render_to_response(context)
