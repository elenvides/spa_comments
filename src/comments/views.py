from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CommentsListView(ListView):
    model = Comment
    template_name = 'comments/comments_list.html'
    context_object_name = 'comments'
    paginate_by = 5

    def get_queryset(self):
        # Getting sort params from URL. default: "-created_at" (LIFO)
        sort_by = self.request.GET.get('sort_by', '-created_at')
        order = self.request.GET.get('order', 'desc')

        # check if sort params
        if sort_by not in ['user__username', 'user__email', 'created_at']:
            sort_by = '-created_at'

        # Determine the sorting order
        if order == 'asc':
            sort_by = sort_by.lstrip('-')
        else:
            sort_by = '-' + sort_by.lstrip('-')

        # Sort main comments using params.
        return super().get_queryset().filter(parent_comment__isnull=True).order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', '-created_at')
        context['order'] = self.request.GET.get('order', 'desc')
        if 'form' not in context:
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
        context = self.get_context_data(object_list=self.object_list, form=form if form else CommentForm())
        return self.render_to_response(context)
