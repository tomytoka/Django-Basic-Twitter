from django import forms
from .models import Post,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfilePicForm(forms.ModelForm):
     profile_image= forms.ImageField(label="Profile Picture")
     profile_bio=forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Profile Bio'}))
     homepage_link =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'website link'}))
     instagram_link =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'instagram link'}))
     linkedin_link=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'linkedin link'}))

     class Meta:
        model= Profile
        fields = ('profile_image','profile_bio','homepage_link','instagram_link','linkedin_link')


class PostForm(forms.ModelForm):
    body = forms.CharField(required=True,widget=forms.widgets.Textarea(attrs={"placeholder":"Post text","class":"form-control",}),label="",)

    class Meta:
        model=Post
        exclude=("user","likes")

class SignUpForm(UserCreationForm):
    email=forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    first_name=forms.CharField(label="",max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First name'}))
    last_name=forms.CharField(label="",max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last name'}))
    
    class Meta:
        model = User
        fields=('username','first_name','last_name','email','password1','password2')

    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'User Name'
            self.fields['username'].label = ''
            self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'