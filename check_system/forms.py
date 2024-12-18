from django import forms
from .models import PetsitterCheck, Report, Reject, RejectImage

class PetsitterCheckForm(forms.ModelForm):
    class Meta:
        model=PetsitterCheck
        exclude=["petsitter", "owner", "order", "start_date", "end_date", "rest", "status"]

class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        exclude=["petsitter_check", "analysis"]

class RejectForm(forms.ModelForm):
    class Meta:
        model=Reject
        exclude=["system", "timestamp", "status"]

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

class RejectImageForm(forms.Form):
    images = MultipleFileField(label='Select files', required=False)
