import os
from selenium.webdriver.common.keys import Keys
# Import the models
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the forms
from lememe.forms import UserForm, UserProfileForm, PostForm, CommentForm,\
    UpdateUserSettingsForm, UpdateUserProfileSettingsForm, PasswordChangeCustomForm

def login(self):
    self.browser.get(self.live_server_url + '/admin/')

    # Types username and password
    username_field = self.browser.find_element_by_name('username')
    username_field.send_keys('admin')

    password_field = self.browser.find_element_by_name('password')
    password_field.send_keys('admin')
    password_field.send_keys(Keys.RETURN)


def user_login(self, username='admin', password='admin'):
    # Types username and password
    username_field = self.browser.find_element_by_name('username')
    username_field.send_keys(username)

    password_field = self.browser.find_element_by_name('password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)


def create_pages(categories):
    # List of pages
    pages = []

    # For each category create 2 pages
    for i in range (0, len(categories)):
        category = categories[i]

        # Name the pages according to the links and create a fake url
        for j in range(0, 2):
            page_number = i * 2 + j + 1
            page = Page(category=category, title="Page " + str(page_number),
                        url="http://www.page" + str(page_number) + ".com", views=page_number)
            page.save()
            pages.append(page)

    return pages

def create_user(username="testuser", password="test1234"):
    # Create a user
    from lememe.models import User, UserProfile
    user = User.objects.get_or_create(username=username, password=password,
                                      first_name="Test", last_name="User", email="testuser@testuser.com")[0]
    user.set_password(user.password)
    user.save()

    # Create a user profile
    user_profile = UserProfile.objects.get_or_create(user=user,
                                                     website="http://www.testuser.com")[0]
    user_profile.save()

    return user, user_profile

