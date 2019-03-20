#Test imports
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




class LememeLiveServerTestsRI(StaticLiveServerTestCase):

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
        super(LememeLiveServerTestsRI, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def test_category_page_appears_when_clicked(self):
        print("here")
        # Go to Lememe main page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        print(url)

        categories = self.browser.find_elements_by_class_name(name="text-dark")
        for cat in categories:
            print(1)
            print(cat)
            cat.click()
            self.assertEqual(url + reverse('lememe:category', args=[cat]), self.browser.current_url)
            cat.click()
