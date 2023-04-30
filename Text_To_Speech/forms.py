from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()
    language = forms.ChoiceField(choices=[('en', 'English'), ('de', 'German'), ('fr', 'French')])
    
    def clean_file(self):
        file = self.cleaned_data['file']
        content_type = file.content_type.split('/')[0]
        if content_type != 'text':
            raise forms.ValidationError('File type is not supported.')
        return file


    