from django import forms
from django.contrib.auth.models import User
from lememe.models import UserProfile, Post, Comment, Preference, Category


# class CategoryForm(forms.ModelForm):
#     name = forms.CharField(max_length=Category.max_length, help_text="Please enter the category name.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     slug = forms.CharField(widget=forms.HiddenInput(), required=False)
#
#     # An inline class to provide additional information on the form.
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Category
#         fields = ('name',)

class PostForm(forms.ModelForm):
    # title = forms.CharField(max_length=128, help_text="Please enter the title of the post.")
    # category = forms.ModelChoiceField(queryset=Category.objects.all(),help_text="Category")
    # image = forms.FileInput()
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:

        # Provide an association between the ModelForm and a model
        model = Post
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them.
        # exclude = ["category",]
        exclude = ('client_id','id','date','user','views')
        # exclude = []
        # fields = (
        #     'title',
        #     'category',
        #     'image',
        # )
        # or specify the fields to include (i.e. not include the category field)
        # fields = ('title', 'url', 'views')




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'website', 'picture')
