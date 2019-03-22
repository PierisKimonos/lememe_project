# Lememe Tests
import os, socket, time
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.core.urlresolvers import reverse
import lememe.test_utils as tu
from django.contrib.auth.models import User
# Import the models
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the forms
from lememe.forms import UserForm, UserProfileForm, PostForm, CommentForm, \
    UpdateUserSettingsForm, UpdateUserProfileSettingsForm, PasswordChangeCustomForm


from lememe.tests_lememe import skip_test

# DECORATORS
def skip_test(self):
    pass


def print_tests_name(self):
    print(self.__name__)
    return self


class LememeLiveServerTests(StaticLiveServerTestCase):

    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser(username='admin', password='admin', email='admin@me.com')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(3)
        self.browser.set_window_size(1800, 800)

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(LememeLiveServerTests, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()



    def test_popup_after_pressing_submit(self):
        #Go to lememe index page page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')

        #Create objects
        user = User.objects.get(username='admin')
        testCategory = Category.objects.create(user=user, name="TestCategory", picture="noFile.jpg")
        post = Post.objects.create(user=user,category=testCategory, client_id="52db56c0",title="test",image="noFile.jpg")

        #Go to lememe post page
        self.browser.get(url+reverse('lememe:index')+"post/52db56c0")
        popup = self.browser.find_elements_by_id('disabled_comment_btn')
        text = (popup[0].get_attribute("data-content"))
        self.assertEqual(text, "Please <a href='/lememe/login/'>login</a> in order to comment.")

        
    def test_comment_submits_properly(self):
        #Go to lememe index page page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')

        # Go to Lememe login page
        self.browser.get(url + reverse('lememe:login'))

        # Create a new test user in database
        username = 'testUser'
        password = 'test1234'
        user = tu.create_user(username=username, password=password)

        # Fill Login form
        # username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(username)

        # password
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(password)

        # Submit
        self.browser.find_element_by_css_selector(".btn-login").click()
        #Create objects
        testCategory = Category.objects.create(user=user[0], name="TestCategory", picture="noFile.jpg")
        post = Post.objects.create(user=user[0],category=testCategory, client_id="52db56c0",title="test",image="noFile.jpg")
    
        #Go to lememe post page
        self.browser.get(url+reverse('lememe:index')+"post/52db56c0")

        #Find comment element and submit text
        text = self.browser.find_element_by_name("text")
        text.send_keys("hello this is my test comment")
        self.browser.find_element_by_class_name("btn-primary").click()

        #At this point im getting a response from ajax but im getting a server error 
        #text = self.browser.find_element_by_class_name("card-text")
        time.sleep(5)

        

        
 

