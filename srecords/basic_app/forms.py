from django import forms
from django.core import validators

class newStudent(forms.Form):
    sid = forms.IntegerField(label='Student ID')
    firstname = forms.CharField(label='First Name')
    lastname = forms.CharField(label='Last Name')
    personal_photo = forms.FileField()
    #birth_certificate = forms.ImageField()
    


class newCourse(forms.Form):
    year = forms.IntegerField(label='Year')
    semester = forms.CharField(label='Semester')
    cid = forms.CharField(label='Course ID')
    name = forms.CharField(label='Course Name')
    price = forms.IntegerField(label='Course Price')
    grade = forms.IntegerField(label='Course Grade')
    
class newFinance(forms.Form):
    pass