from django.core.exceptions import ValidationError

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from bs4 import BeautifulSoup


allowed_tags = ['a', 'code', 'i', 'strong']
allowed_attributes = {
    'a': ['href', 'title'],
}


def clean_html(input_text):
    soup = BeautifulSoup(input_text, 'html.parser')
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.hidden = True
        tag.attrs = {name: value for name, value in tag.attrs.items() if name in allowed_attributes.get(tag.name, [])}
    return soup.renderContents().decode('utf8')


def file_size_validator(value):
    max_file_size = 102400  # 100 KB
    if value.size > max_file_size:
        raise ValidationError(f'The file is too big. Max allowed - {max_file_size / 1024} KB.')


def image_size_validator(value):
    max_file_size = 1024 * 1024  # 1 MB
    if value.size > max_file_size:
        raise ValidationError(f'The file is too big. Max allowed  - {max_file_size / 1024 / 1024} MB.')


def validate_image(image):
    try:
        img = Image.open(image)
        if img.format not in ('JPEG', 'PNG', 'GIF'):
            raise ValidationError('Unsupportable format')
        if img.width > 320 or img.height > 240:
            img = img.resize((320, 240), Image.ANTIALIAS)
        buffer = BytesIO()
        img.save(fp=buffer, format=img.format)
        return InMemoryUploadedFile(
            buffer, 'ImageField', image.name, 'image/%s' % img.format.lower(), buffer.getbuffer().nbytes, None
        )
    except Exception as e:
        raise ValidationError(str(e))


def validate_file(file):
    if file.size > 100 * 1024 or not file.name.endswith('.txt'):
        raise ValidationError('Unsupportable text file')
