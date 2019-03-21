# Lememe Tests
import os, socket
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import lememe.test_utils as tu
# Import the models
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the forms
from lememe.forms import UserForm, UserProfileForm, PostForm, CommentForm,\
    UpdateUserSettingsForm, UpdateUserProfileSettingsForm, PasswordChangeCustomForm

def skip_test(self):
    pass

class LememeTests(TestCase):
    @skip_test
    def test_login_form_is_displayed_correctly(self):
        #Access login page
        try:
            response = self.client.get(reverse('lememe:register'))
        except:
            return False

        #Check form display
        #Header
        self.assertIn('Welcome'.lower(), response.content.decode('ascii').lower())
        self.assertIn('back to'.lower(), response.content.decode('ascii').lower())

        #Username label and input text
        self.assertIn('>Username</label>', response.content.decode('ascii'))
        self.assertIn('input type="text"', response.content.decode('ascii'))
        self.assertIn('name="username"', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        #Password label and input text
        self.assertIn('>Password</label>', response.content.decode('ascii'))
        self.assertIn('input type="password"', response.content.decode('ascii'))
        self.assertIn('name="password"', response.content.decode('ascii'))
        self.assertIn('value=""', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        #Submit button
        self.assertIn('input type="submit"', response.content.decode('ascii'))
        self.assertIn('value="submit"', response.content.decode('ascii'))


class LememeLiveServerTests(StaticLiveServerTestCase):

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
        super(LememeLiveServerTests, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    @skip_test
    def test_navigate_from_about_to_index_when_clicking_logo(self):
        # Go to Lememe main page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('lememe:about'))

        # Check if there is a link back to the home page
        brand_logo = self.browser.find_element_by_class_name(name="navbar-brand")
        brand_logo.click()

        # Check if it goes back to the home page
        self.assertEqual(url + reverse('lememe:index'), self.browser.current_url)


    def test_login_no_such_user_exists(self):
        # Go to Lememe login page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('lememe:login'))

        # Create a new test user in database
        username = 'testUser'
        password = 'test1234'
        wrong_username = 'Daniel'
        tu.create_user(username=username, password=password)

        # Try to log in as that user through the login form

        # Fill Login form
        # username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(wrong_username)  # wrong username

        # password
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('345677')  # wrong password

        # Submit
        self.browser.find_element_by_css_selector(".btn-login").click()

        # Check if body now has welcome message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(('*no user with this username "%s" exists'%wrong_username).lower(), body.text.lower())


    def test_login_combination_correct_username_wrong_password_doesnot_match(self):
        # Go to Lememe login page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('lememe:login'))

        # Create a new test user in database
        username = 'testUser'
        password = 'test1234'
        tu.create_user(username=username, password=password)

        # Try to log in as that user through the login form

        # Fill Login form
        # username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(username)

        # password
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('345677')  # wrong password

        # Submit
        self.browser.find_element_by_css_selector(".btn-login").click()

        # Check if body now has welcome message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(('The combination does not match').lower(), body.text.lower())

    @skip_test
    def test_correct_login_credentials_work(self):
        # Go to Lememe login page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('lememe:login'))

        # Create a new test user in database
        username = 'testUser'
        password = 'test1234'
        tu.create_user(username=username, password=password)

        # Try to log in as that user through the login form

        # Fill Login form
        # username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(username)

        # password
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(password)

        # Submit
        self.browser.find_element_by_css_selector(".btn-login").click()

        # Check if body now has welcome message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(('Welcome back %s'%username).lower(), body.text.lower())

