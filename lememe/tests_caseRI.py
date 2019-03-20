#Test imports
import os, socket, time
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from django.core.urlresolvers import reverse
import lememe.test_utils as tu
# Import the models
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the forms
from lememe.forms import UserForm, UserProfileForm, PostForm, CommentForm,\
    UpdateUserSettingsForm, UpdateUserProfileSettingsForm, PasswordChangeCustomForm
from lememe.tests_lememe import skip_test


class LememeLiveServerTestsRI(StaticLiveServerTestCase):

    def setUp(self):
        User.objects.create_superuser(username='admin', password='admin', email='admin@me.com')
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('headless')
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
        print(url)
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('lememe:index'))

        user = User.objects.get(username='admin')

        #create categories for the database
        # Create categories from 1 to 10
        categories = []
        for i in range(1, 11):
            categories.append(Category.objects.get_or_create(user=user, name="Category " + str(i), picture="noFile.jpg")[0])

        print(Category.objects.all().count())
        print(len(categories))

        try:
            response = self.client.get(reverse('lememe:register'))
        except:
            return False

        print(response)
        print(reverse('lememe:index'))

        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        print(url + reverse('lememe:index'))
        self.browser.get(url + reverse('lememe:index'))



        body = self.browser.find_element_by_tag_name('body')

        print(body.text.lower())
        input()
        listB = []
        # for i in body.text:
        #     listB.append(i)
        #     print(listB)
        # categories = self.browser.find_elements_by_class_name(name="text-dark")
        categories = self.browser.find_elements_by_xpath("//a[contains(text(), 'Category')]")
        print(categories)
        print("HEREEE")
        input()
        for cat in categories:
            cat.click()
            time.sleep(3)

        #categories = self.browser.find_elements_by_xpath('//a[@href="'"/lememe/category/"'"]')
        #categories = self.browser.find_element_by_xpath("//a[contains(text(), 'category')]")
        print(categories.text.lower())
        print("cats:",categories)
        for cat in body and body[0]== "category":
            print(1)
            print(cat)
            cat.click()
            self.assertEqual(url + reverse('lememe:category', args=[cat]), self.browser.current_url)

    @skip_test
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
        self.assertIn(("No results found for \"%s\""%search_var).lower(), body.text.lower())
