from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.ModelForm):
    parent_comment = forms.ModelChoiceField(queryset=Comment.objects.all(), widget=forms.HiddenInput(), required=False)
    text = forms.CharField(
        label=_("Comment"),
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        help_text=_("You can use the following HTML tags: &lt;a&gt; &lt;code&gt; &lt;i&gt; &lt;strong&gt;"),
    )

    class Meta:
        model = Comment
        fields = ['parent_comment', 'text', 'image', 'file']

    def clean_text(self):
        from .validators import clean_html
        text = self.cleaned_data.get('text')
        return clean_html(text)
