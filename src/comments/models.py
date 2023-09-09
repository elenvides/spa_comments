from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

from comments.validators import image_size_validator, file_size_validator, validate_image, validate_file


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.RESTRICT, related_name='replies')

    image = models.ImageField(upload_to='media/images/', null=True, blank=True,
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif']),
                                          image_size_validator,
                                          validate_image])  # Added validate_image here
    file = models.FileField(upload_to='media/files/', null=True, blank=True,
                            validators=[FileExtensionValidator(['txt']),
                                        file_size_validator,
                                        validate_file])  # Added validate_file here

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created_at}'
