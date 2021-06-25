from django.test import Client, TestCase
from django.urls import reverse
from events.tests.factories import EventFactory
from users.tests.factories import ProfileRegistrationDataFactory, VoluntaryFactory, BenefactorFactory


class EventListViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = ProfileRegistrationDataFactory().user
        cls.default_passwd = 'django01'
        cls.user.set_password(cls.default_passwd)
        cls.user.save()

    def setUp(self):
        self.client = Client()
        self.events = EventFactory.create_batch(10)
        self.url = reverse('events:list')

    def test_get_without_login(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_get_with_login(self):
        self.client.login(username=self.user.username,
                          password=self.default_passwd)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/list.html')

    def test_post_with_login(self):
        self.client.login(username=self.user.username,
                          password=self.default_passwd)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/list.html')


class EventDeleteViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = ProfileRegistrationDataFactory().user
        cls.default_passwd = 'django01'
        cls.user.set_password(cls.default_passwd)
        cls.user.save()

    def setUp(self):
        self.client = Client()
        self.event = EventFactory()
        self.url = reverse('events:delete', kwargs={'pk': self.event.pk})

    def test_get_without_login(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(self.event.__class__.objects.count(), 1)

    def test_get_with_login(self):
        self.client.login(username=self.user.username,
                          password=self.default_passwd)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.event.__class__.objects.count(), 1)

    def test_post_with_login(self):
        self.client.login(username=self.user.username,
                          password=self.default_passwd)

        response = self.client.post(self.url)
        events_url = reverse('events:list')
        self.assertRedirects(response, events_url)
        self.assertEqual(self.event.__class__.objects.count(), 0)


class EventCreateViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = ProfileRegistrationDataFactory().user
        cls.default_passwd = 'django01'
        cls.user.set_password(cls.default_passwd)
        cls.user.save()

    def setUp(self):
        self.client = Client()
        self.url = reverse('events:create')

    def test_get_without_login(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_get_with_login(self):
        self.client.login(username=self.user.username,
                          password=self.default_passwd)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create.html')

    def test_post_with_login(self):
        self.client.login(username=self.user.username,
                          password=self.default_passwd)

        event = EventFactory.build()
        volunteers = VoluntaryFactory.create_batch(10)
        context = {
            'event_name': event.event_name,
            'start_date': event.start_date,
            'event_details': event.event_details,
            'volunteers': [v.pk for v in volunteers],
            'materials': event.materials,
        }

        response = self.client.post(self.url, context)
        events_url = reverse('events:list')
        self.assertRedirects(response, events_url)
        self.assertEqual(event.__class__.objects.count(), 1)


class EventUpdateViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = ProfileRegistrationDataFactory().user
        cls.default_passwd = 'django01'
        cls.user.set_password(cls.default_passwd)
        cls.user.save()

    def setUp(self):
        self.client = Client()
        self.event = EventFactory()
        self.url = reverse('events:update', kwargs={'pk': self.event.pk})

    def test_get_without_login(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_get_with_login(self):
        self.client.login(username=self.user.username,
                          password=self.default_passwd)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create.html')

    def test_post_with_login(self):
        self.client.login(username=self.user.username,
                          password=self.default_passwd)

        event = EventFactory.build()
        volunteers = VoluntaryFactory.create_batch(10)
        context = {
            'event_name': event.event_name,
            'start_date': event.start_date,
            'event_details': event.event_details,
            'volunteers': [v.pk for v in volunteers],
        }

        response = self.client.post(self.url, context)
        events_url = reverse('events:list')
        self.assertRedirects(response, events_url)
        self.assertEqual(event.__class__.objects.count(), 1)
