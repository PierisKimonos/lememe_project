# Lememe Tests
import os, socket
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
# Import the models
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the forms
from lememe.forms import UserForm, UserProfileForm, PostForm, CommentForm,\
    UpdateUserSettingsForm, UpdateUserProfileSettingsForm, PasswordChangeCustomForm

from lememe.decorators import skip_test

class Chapter7LiveServerTestCase(StaticLiveServerTestCase):

    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser(username='admin', password='admin', email='admin@me.com')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options = chrome_options)
        self.browser.implicitly_wait(3)

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(Chapter7LiveServerTestCase, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()


class Chapter7ViewTests(TestCase):

    def category_page_appears_when_clicked(self):
        print("here")
        # Go to Lememe main page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        print(url)

        categories = self.browser.find_elements_by_class_name(name="text-dark")
        for cat in categories:
            print(cat)
            cat.click()
            self.assertEqual(url + reverse('lememe:category', args=[cat]), self.browser.current_url)
        cat.click()

        # Check if it goes to the category page