from django import forms
from .models import PetsitterCheck, Report, Reject


class PetsitterCheckForm(forms.ModelForm):
    class Meta:
        model=PetsitterCheck
        fields=[
            "frequency",
            "interval",
            "start_time"
        ]

class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        fields=[
            "text",
            "image",
            "video"
        ]

        def clean_image(self):
            image = self.cleaned_data.get("image")
            if image:
                valid_extensions = ['.jpg', '.jpeg', '.png']
                extension = image.name.split('.')[-1].lower()
                if f'.{extension}' not in valid_extensions:
                    raise forms.ValidationError('Недопустимый формат изображения. Допустимые форматы: jpg, jpeg, png.')

                max_size = 5 * 1024 * 1024
                if image.size > max_size:
                    raise forms.ValidationError('Размер изображения не должен превышать 5 MB.')

        def clean_video(self):
            video = self.cleaned_data.get("video")
            if video:
                valid_extensions = ['.mp4', '.avi', '.mov', '.mkv']
                extension = video.name.split('.')[-1].lower()
                if f'.{extension}' not in valid_extensions:
                    raise forms.ValidationError('Недопустимый формат видео. Допустимые форматы: mp4, avi, mov, mkv.')

                max_size = 10 * 1024 * 1024  
                if video.size > max_size:
                    raise forms.ValidationError('Размер видео не должен превышать 10 MB.')

            return video

class RejectForm(forms.ModelForm):
    class Meta:
        model=Reject
        fields=[
            "text",
            "video"
        ]

        def clean_video(self):
            video = self.clean_data.get("video")
            if video:
                valid_extensions = ['.mp4', '.avi', '.mov', '.mkv']
                extension = video.name.split('.')[-1].lower()
                if f'.{extension}' not in valid_extensions:
                    raise forms.ValidationError('Недопустимый формат видео. Допустимые форматы: mp4, avi, mov, mkv.')

                max_size = 10 * 1024 * 1024  
                if video.size > max_size:
                    raise forms.ValidationError('Размер видео не должен превышать 10 MB.')
            return video
                

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

    def clean_images(self):
        images = self.cleaned_data.get("images", [])
        if images:
            if len(images) > 5:
                raise forms.ValidationError("Избыточное количество фотографий.")
            
            valid_extensions = [".jpeg", ".jpg", ".png"]
            max_size = 5 * 1024 * 1024
            for image in images:
                extension = image.name.split(".")[-1].lower()
                if extension not in valid_extensions:
                    raise forms.ValidationError('Недопустимый формат изображения. Допустимые форматы: jpg, jpeg, png.')
                
                if image.size > max_size:
                    raise forms.ValidationError('Размер изображения не должен превышать 5 MB.')
                
        return images
            
