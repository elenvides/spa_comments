from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from PIL import Image

from comments.validators import file_size_validator


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.RESTRICT, related_name='replies')

    image = models.ImageField(upload_to='images/', null=True, blank=True,
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])])
    file = models.FileField(upload_to='files/', null=True, blank=True,
                            validators=[FileExtensionValidator(['txt']), file_size_validator])

    class Meta:
        db_table = "comments"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 240 or img.width > 320:
                output_size = (320, 240)
                img.thumbnail(output_size, Image.LANCZOS)
                img.save(self.image.path)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created_at}'
