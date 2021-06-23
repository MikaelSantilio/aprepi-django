from django.test import Client, TestCase
from django.urls import reverse
from events.tests.factories import EventFactory
from users.tests.factories import ProfileRegistrationDataFactory, VoluntaryFactory


class MakeDonationEventViewTestCase(TestCase):
    pass


class EventListViewTestCase(TestCase):
    pass


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

    def test_get_with_login(self):
        self.client.login(username=self.user.username, password=self.default_passwd)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/delete.html')

    def test_post_with_login(self):
        self.client.login(username=self.user.username, password=self.default_passwd)

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
        # event_obj = evevent.objects.all().last()
        events_url = reverse('events:list')
        self.assertRedirects(response, events_url)


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
        self.client.login(username=self.user.username, password=self.default_passwd)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create.html')

    def test_post_with_login(self):
        self.client.login(username=self.user.username, password=self.default_passwd)

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
        # event_obj = evevent.objects.all().last()
        events_url = reverse('events:list')
        self.assertRedirects(response, events_url)


class EventUpdateViewTestCase(TestCase):
    pass


class EventListViewTestCase(TestCase):
    pass
