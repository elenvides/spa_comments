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
