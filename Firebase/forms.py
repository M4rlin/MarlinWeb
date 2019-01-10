from django import forms
from django.forms import ModelForm
from .models import *
UserType_Questions = (
    ('' ,"-----------"),
    ('I', 'Identification'),
    ('M', 'Multiple Choice'),
    ('T', 'True or False')
)

UserType_TF = (
    ('' ,"-----------"),
    ('T', 'True'),
    ('F', 'False'),
)

Section = (
    ('' ,"-----------"),
    ('N1', 'N1'),
    ('ZC11', 'ZC11'),
    ('ZT11', 'ZT11'),
    ('ZT12', 'ZT12'),
    ('ZT13', 'ZT13')
)
Subjects = (
    ('' ,"-----------"),
    ('CSDC101', 'CSDC101'),
    ('ICST101', 'ICST101'),
)

Gender = (
    ('' ,"-----------"),
    ('M', 'Male'),
    ('F', 'Female'),
)

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','id':'username','placeholder':'Email Address'}),label='Email address',max_length=75, required=True)
    password = forms.CharField(label='Password', max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'username'}))

class UserForm(forms.Form):
    Student_Fname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="First Name:")
    Student_Lname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Last Name:")
    Student_Age = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Age:")
    Gender = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=Gender,label="Gender:" )
    Student_Section = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=Section,label="Section:",required=False )
    Student_Subject = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=Subjects,label="Subject Code:",required=False )

class upload(forms.Form):
    file = forms.FileField()

class TimeInput(forms.TimeInput):
    input_type = 'time'

class DateInput(forms.DateInput):
    input_type = 'date'


class FeedBackForm(ModelForm):
    class Meta:
        model = feedback
        # fields = ['username', 'password', 'User_LastName','User_FirstName']
        fields = '__all__'
        widgets = {
        "email":forms.TextInput(attrs={'class':'form-control','id':'username','placeholder':'Email Address'}),
        "subject":forms.TextInput(attrs={'class':'form-control','id':'suggest_form','placeholder':'Subject'}),
        "suggestion":forms.Textarea(attrs={'class':'form-control','id':'username','placeholder':'Feedback','cols': 30, 'rows': 3}),
        }


class PreferedTimeForm(forms.Form):
    preferedTime1 = forms.TimeField(widget=TimeInput(format='%H:%M',attrs={'class':'form-control'}),label="Prefered Time 1")
    preferedTime2 = forms.TimeField(widget=TimeInput(format='%H:%M',attrs={'class':'form-control',}),label="Prefered Time 2")
    preferedTime3 = forms.TimeField(widget=TimeInput(format='%H:%M',attrs={'class':'form-control',}),label="Prefered Time 3")
    preferedTime4 = forms.TimeField(widget=TimeInput(format='%H:%M',attrs={'class':'form-control',}),label="Prefered Time 4")
    preferedTime5 = forms.TimeField(widget=TimeInput(format='%H:%M',attrs={'class':'form-control',}),label="Prefered Time 5")

class TeacherForm(forms.Form):
    Student_Fname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="First Name:",required=False)
    Student_Lname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Last Name:",required=False)
    Student_Age = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Age:",required=False)
    Student_Section = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=Section,label="Section:",required=False )
    Student_Subject = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=Subjects,label="Subject Code:",required=False )

class QuizInfoForm(forms.Form):
    Quiz_Date = forms.DateField(widget=DateInput(format='%Y-%m-%d',attrs={'class':'form-control',}),label="Quiz Date")
    Quiz_Topic = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Quiz Topic:",help_text='')
    Sections = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=Section,label="Section:",required=False )
    Subjects = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=Subjects,label="Subject Code",required=False )

class Identity1(forms.Form):
    IdentNum1_1 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'Identity1'}),label="Item 1:",required=False)
    IdentAnswer_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Answer:",required=False)

class Identity2(forms.Form):
    IdentNum1_2 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'Identity2'}),label="Item 2:",required=False)
    IdentAnswer_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Answer:",required=False)

class Identity3(forms.Form):
    IdentNum1_3 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'Identity3'}),label="Item 3:" ,required=False)
    IdentAnswer_3 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Answer:" ,required=False)

class Identity4(forms.Form):
    IdentNum1_4 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'Identity4'}),label="Item 4:",required=False )
    IdentAnswer_4 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Answer:",required=False )

class Identity5(forms.Form):
    IdentNum1_5 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'Identity5'}),label="Item 5:",required=False)
    IdentAnswer_5 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}),label="Answer:",required=False)

class Multiple1(forms.Form):
    MultipleChoice_Question1 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'MC1'}),label="Item 1:",required=False)

class Multiple2(forms.Form):
    MultipleChoice_Question2 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'MC2'}),label="Item 2:",required=False)


class Multiple3(forms.Form):
    MultipleChoice_Question3 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'MC3'}),label="Item 3:",required=False)


class Multiple4(forms.Form):
    MultipleChoice_Question4 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'MC4'}),label="Item 4:",required=False)


class Multiple5(forms.Form):
    MultipleChoice_Question5 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'MC5'}),label="Item 5:",required=False)


class TF1(forms.Form):
    Tf_Question1 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'TF1'}),label="Item 1:" ,required=False)
    Tf_Answer1 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=UserType_TF,label="Answer:",required=False )


class TF2(forms.Form):
    Tf_Question2 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'TF2'}),label="Item 2:" ,required=False)
    Tf_Answer2 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=UserType_TF,label="Answer:",required=False )

class TF3(forms.Form):
    Tf_Question3 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'TF3'}),label="Item 3:" ,required=False)
    Tf_Answer3 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=UserType_TF,label="Answer:",required=False )

class TF4(forms.Form):
    Tf_Question4 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'TF4'}),label="Item 4:" ,required=False)
    Tf_Answer4 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=UserType_TF,label="Answer:",required=False )

class TF5(forms.Form):
    Tf_Question5 = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'TF5'}),label="Item 5:" ,required=False)
    Tf_Answer5 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',}), choices=UserType_TF,label="Answer:",required=False )

class ItemNum2_InfoForm(forms.Form):
    ItemNum1_2 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','id':'choices1',}), choices=UserType_Questions,label="Question Type:",required=False )

class ItemNum3_InfoForm(forms.Form):
    ItemNum1_3 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','id':'choices2',}), choices=UserType_Questions,label="Question Type:", required=False)

class ItemNum4_InfoForm(forms.Form):
    ItemNum1_4 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','id':'choices3',}), choices=UserType_Questions,label="Question Type:", required=False)

class ItemNum5_InfoForm(forms.Form):
    ItemNum1_5 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','id':'choices4',}), choices=UserType_Questions,label="Question Type:", required=False)

class ItemNum1_InfoForm(forms.Form):
    ItemNum1_1 = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','id':'choices',}), choices=UserType_Questions,label="Question Type:", required=False,)