from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase, RequestFactory
from django.test.client import Client


class BaseTemplateTest(SimpleTestCase):
    client = Client()

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # Create a throwaway user object.
        self.user = User.objects.create_user(
            username='john', email='john@email.com', password='secret')

    def tearDown(self):
        # Delete the user after each test case.
        self.user.delete()

    def test_base_template_render(self):
        """Test that the base template renders with expected content.
        """
        url = reverse('test_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webtemplate_dpaw/base.html')
        self.assertContains(response, '<li class="active"><a href="#">Link 1</a></li>')
        self.assertContains(response, '<a id="id_a_login" href="/login/">Log in</a>')

    def test_base_template_logged_in(self):
        """Test the base template displays a 'Log out' link for logged-in users.
        """
        url = reverse('test_page')
        self.client.login(username='john', password='secret')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(url)
        self.assertContains(response, '<a id="id_a_logout" href="/logout/">Log out</a>')
        self.assertNotContains(response, 'Log in')

    def test_base_template_extend(self):
        """Test that the base template renders, with some content overridden.
        """
        url = reverse('test_page_2')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 id="id_hello_world">Hello, World!</h1>')
