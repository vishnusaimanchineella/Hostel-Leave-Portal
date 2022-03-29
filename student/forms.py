from django import forms
from student.models import Department,Student
from django.contrib.auth.models import User


# EMPLoYEE
class StudentCreateForm(forms.ModelForm):
	studentid = forms.CharField(widget=forms.TextInput(attrs={}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':'previewImage(this);'}))
	class Meta:
		model = Student
		exclude = ['is_blocked','is_deleted','created','updated']
		widgets = {
				'bio':forms.Textarea(attrs={'cols':5,'rows':5})
		}

