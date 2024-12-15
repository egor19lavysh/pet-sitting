from django import forms
from .models import Review, ReviewImage, Reply
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):
    score = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}))

    class Meta:
        model=Review
        exclude=["reviewer", "user", "published", "timestamp"]

    def clean(self):
        cd = super().clean()
        if not 1 <= cd["score"] <= 5:
            raise ValidationError("Ваша оценка должна быть в промежутке от 1 до 5 включительно!")


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ReviewImageForm(forms.Form):
    images = MultipleFileField(label='Select files', required=False)


class ReplyForm(forms.ModelForm):
    class Meta:
        model=Reply
        exclude=["timestamp", "review"]