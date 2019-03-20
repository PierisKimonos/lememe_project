from django import forms
from django.contrib.auth.models import User
from lememe.models import UserProfile, Post, Comment, Preference, Category
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'comment-text',
                'required': True,
                'placeholder': 'Enter a comment...',
                'rows': 1,
                'cols': 69
            }),
        }


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
        exclude = ('client_id', 'id', 'date', 'user', 'views')
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


# Update settings form
class UpdateUserSettingsForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]


# Update settings form
class UpdateUserProfileSettingsForm(UserChangeForm):
    password = None

    class Meta:
        model = UserProfile
        fields = [
            'picture',
            'website',
            'bio',
        ]

        
class PasswordChangeCustomForm(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          "Your old password is incorrect. Try again."
                      }
    old_password = forms.CharField(required=True, label='Old Password',
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control'},
                                       render_value=True),
                                   error_messages={
                                       'required': 'Old password field cannot be blank'})

    new_password1 = forms.CharField(required=True, label='New Password',
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control'},
                                        render_value=True),
                                    error_messages={
                                        'required': 'Old password field cannot be blank'})
    new_password2 = forms.CharField(required=True, label='Confirm New Password',
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control'},
                                        render_value=True),
                                    error_messages={
                                        'required': 'Old password field cannot be blank'})

    def clean(self):
        cd = self.cleaned_data
        if cd.get('new_password1') != cd.get('new_password2'):
            self.add_error('new_password2', "passwords do not match !")
            # raise forms.ValidationError('password mismatch')
        return cd

    def clean_new_password2(self):
        password2 = self.cleaned_data.get("new_password2", "")
        if not password2:  # If both passwords has value
            raise forms.ValidationError(_(u"Passwords can't be blank."))
        return password2
