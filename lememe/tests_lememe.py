# Lememe Tests
import os, socket, time
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.core.urlresolvers import reverse
import lememe.test_utils as tu
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Import the models
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the forms
from lememe.forms import UserForm, UserProfileForm, PostForm, CommentForm, \
    UpdateUserSettingsForm, UpdateUserProfileSettingsForm, PasswordChangeCustomForm


# DECORATORS
def skip_test(self):
    pass


def print_tests_name(self):
    print(self.__name__)
    return self


# TESTS
class LememeTests(TestCase):

    def test_registration_form_is_displayed_correctly(self):
        # Access registration page
        try:
            response = self.client.get(reverse('lememe:register'))
        except:
            return False

        # Check if form is rendered correctly
        self.assertIn('<h1>Register for Lememe</h1>'.lower(), response.content.decode('ascii').lower())

        # Check form in response context is instance of UserForm
        self.assertTrue(isinstance(response.context['user_form'], UserForm))

        user_form = UserForm()

        # Check form is displayed correctly
        self.assertEquals(response.context['user_form'].as_p(), user_form.as_p())

        # Check submit button
        self.assertIn('type="submit"', response.content.decode('ascii'))
        self.assertIn('name="submit"', response.content.decode('ascii'))
        self.assertIn('value="Register"', response.content.decode('ascii'))

    def test_login_form_is_displayed_correctly(self):
        # Access login page
        try:
            response = self.client.get(reverse('lememe:login'))
        except:
            return False

        # Check form display
        # Header
        self.assertIn('Welcome'.lower(), response.content.decode('ascii').lower())
        self.assertIn('back to'.lower(), response.content.decode('ascii').lower())

        # Username label and input text
        self.assertIn('>Username</label>', response.content.decode('ascii'))
        self.assertIn('input type="text"', response.content.decode('ascii'))
        self.assertIn('name="username"', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        # Password label and input text
        self.assertIn('>Password</label>', response.content.decode('ascii'))
        self.assertIn('input type="password"', response.content.decode('ascii'))
        self.assertIn('name="password"', response.content.decode('ascii'))
        self.assertIn('value=""', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        # Submit button
        self.assertIn('input type="submit"', response.content.decode('ascii'))
        self.assertIn('value="submit"', response.content.decode('ascii'))


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
        self.assertIn(('Welcome back %s' % username).lower(), body.text.lower())

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
        self.assertIn(('*no user with this username "%s" exists' % wrong_username).lower(), body.text.lower())

    def test_login_combination_correct_username_wrong_password_does_not_match(self):
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

    def test_register_user(self):
        # Go to Lememe Registration page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('lememe:register'))

        username = 'testUser'
        password = 'test1234'

        # Fill registration form
        # username
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys(username)

        # password
        password_field = self.browser.find_element_by_id('id_password')
        password_field.send_keys(password)

        # first name
        firstname_field = self.browser.find_element_by_id('id_first_name')
        firstname_field.send_keys('Test')

        # last name
        lastname_field = self.browser.find_element_by_id('id_last_name')
        lastname_field.send_keys('User')

        # email
        email_field = self.browser.find_element_by_id('id_email')
        email_field.send_keys('testuser@testuser.com')

        # bio
        bio_field = self.browser.find_element_by_id('id_bio')
        bio_field.send_keys("Test User's Bio")

        # website
        website_field = self.browser.find_element_by_id('id_website')
        website_field.send_keys('http://www.testuser.com')

        # Submit
        website_field.send_keys(Keys.RETURN)

        # Check we are on Login Page now
        self.assertEquals(self.browser.current_url, url + reverse('lememe:login'));

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
        self.assertIn(('Welcome back %s' % username).lower(), body.text.lower())

    def test_category_page_appears_when_clicked(self):
        # Go to Lememe main page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('lememe:index'))

        user = User.objects.get(username='admin')

        # Create categories from 1 to 10
        categories = []
        for i in range(1, 11):
            c = Category.objects.get_or_create(user=user, name="Category " + str(i), picture="noFile.jpg")[0]
            categories.append(c)

        # Refresh page so new categories load
        self.browser.refresh()
        if len(categories) == 0:
            return False

        # for each item in the list
        for cat in categories:
            # Click on the link with that id
            self.browser.find_element_by_id(cat.name).click()
            # Check if the current url is the reversed categories url
            self.assertEqual(url + reverse('lememe:show_category', args=[cat.slug]), self.browser.current_url)

    def test_search_works(self):
        # Go to Lememe login page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url)
        search_var = "x"

        # Enter text in search bar
        search_field = self.browser.find_element_by_id('search_text_input')
        search_field.send_keys(search_var)

        # click search button
        self.browser.find_element_by_id("search_button").click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(("No results found for \"%s\"" % search_var).lower(), body.text.lower())

    def test_categories_exist(self):
        # Go to Lememe main page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('lememe:index'))

        user = User.objects.get(username='admin')

        # Create categories from 1 to 10
        categories = []
        for i in range(1, 11):
            categories.append(
                Category.objects.get_or_create(user=user, name="Category " + str(i), picture="noFile.jpg")[0])

    def test_logout_link(self):
        # Go to Lememe login page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('lememe:login'))
        except:
            return False
        # Log in
        tu.user_login(self)

        # redirect to logout url
        try:
            self.browser.get(url + reverse('lememe:logout'))
        except:
            return False

        # Check we are on homepage
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Welcome to le-Meme'.lower(), body.text.lower())

    def test_popup_after_pressing_submit(self):
        # Go to lememe index page page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')

        # Create objects
        user = User.objects.get(username='admin')
        testCategory = Category.objects.create(user=user, name="TestCategory", picture="noFile.jpg")
        post = Post.objects.create(user=user, category=testCategory, client_id="52db56c0", title="test",
                                   image="noFile.jpg")

        # Go to lememe post page
        self.browser.get(url + reverse('lememe:index') + "post/52db56c0")
        popup = self.browser.find_elements_by_id('disabled_comment_btn')
        text = (popup[0].get_attribute("data-content"))
        self.assertEqual(text, "Please <a href='/lememe/login/'>login</a> in order to comment.")

    def test_comment_submits_properly(self):
        # Go to lememe index page page
        self.client.get(reverse('lememe:index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')

        # Go to Lememe login page
        self.browser.get(url + reverse('lememe:login'))

        # Create a new test user in database
        username = 'testUser'
        password = 'test1234'
        comment = "This a UNIQUE comment to be posted by testUser"
        user = User.objects.get_or_create(username=username)[0]
        user.password = make_password(password)
        user.save()
        user_profile = UserProfile.objects.create(user=user, picture="noFile.jpg")

        # Fill Login form
        # username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(username)

        # password
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(password)

        # Submit
        self.browser.find_element_by_css_selector(".btn-login").click()
        # Create objects
        testCategory = Category.objects.create(user=user, name="TestCategory", picture="noFile.jpg")
        post = Post.objects.create(user=user, category=testCategory, client_id="52db56c0", title="test",
                                   image="noFile.jpg")

        # Go to lememe post page
        self.browser.get(url + reverse('lememe:show_post', args=[post.client_id]))

        # Find comment element and submit text
        text = self.browser.find_element_by_name("text")
        text.send_keys(comment)
        self.browser.find_element_by_class_name("btn-primary").click()
        time.sleep(1)

        # Check if the new comment is present in the page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(comment.lower(), body.text.lower())
