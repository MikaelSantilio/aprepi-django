from rest_framework.test import APIClient, APITransactionTestCase
from events.tests.factories import EventFactory, CostFactory, CollectionFactory
from users.tests.factories import ProfileRegistrationDataFactory
from rest_framework import status
from django.urls import reverse
from events.api.serializers import EventSerializer, CostSerializer, CollectionSerializer


class EventsAPITestCase(APITransactionTestCase):

    def setUp(self):
        self.client = APIClient()

        EventFactory.create_batch(10)
        self.user = ProfileRegistrationDataFactory(user__is_employee=True).user
        self.default_passwd = 'django01'
        self.user.set_password(self.default_passwd)
        self.user.save()

        request_login = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": self.user.username, "password": self.default_passwd}, format="json")

        self.access = request_login.data["access"]
        self.refresh = request_login.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.access)

    def test_events_list(self):

        EventFactory()
        request = self.client.get(reverse("api:events:events-list"))

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 4)

    def test_event_detail(self):

        event = EventFactory()
        request = self.client.get(reverse("api:events:events-detail", kwargs={"pk": event.pk}))

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data, EventSerializer(event).data)

    def test_event_delete(self):
        event = EventFactory()
        request = self.client.delete(reverse("api:events:events-detail", kwargs={"pk": event.pk}))

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(request.data, None)

    def test_event_create(self):
        event_build = EventFactory.build().__dict__
        for key in ("_id", "_state"):
            if key in event_build:
                del event_build[key]

        request = self.client.post(reverse("api:events:events-list"), event_build, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_event_edit(self):

        event = EventFactory()

        event_dict = event.__dict__
        del event_dict["_state"]
        event_dict["event_name"] = "Alteracao"

        request = self.client.put(
            reverse("api:events:events-detail", kwargs={"pk": event.id}), event_dict, format="json")

        self.assertEqual(request.status_code, status.HTTP_200_OK)


class CostAPITestCase(APITransactionTestCase):

    def setUp(self):
        self.client = APIClient()

        self.event = EventFactory()
        self.costs = CostFactory.create_batch(10)
        self.user = ProfileRegistrationDataFactory(user__is_employee=True).user
        self.default_passwd = 'django01'
        self.user.set_password(self.default_passwd)
        self.user.save()

        request_login = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": self.user.username, "password": self.default_passwd}, format="json")

        self.access = request_login.data["access"]
        self.refresh = request_login.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.access)

    def test_cost_list(self):
        request = self.client.get(reverse("api:events:cost-list"))

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 4)

    def test_cost_detail(self):

        cost = self.costs[0]
        request = self.client.get(reverse("api:events:cost-detail", kwargs={"pk": cost.pk}))

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data, CostSerializer(cost).data)

    def test_cost_delete(self):
        cost = self.costs[1]
        request = self.client.delete(reverse("api:events:cost-detail", kwargs={"pk": cost.pk}))

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(request.data, None)

    def test_cost_create(self):
        cost_build = CostFactory.build().__dict__
        for key in ("_id", "_state"):
            if key in cost_build:
                del cost_build[key]
        cost_build["event"] = self.event.id

        request = self.client.post(reverse("api:events:cost-list"), cost_build, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_cost_edit(self):

        cost = self.costs[2]

        cost_dict = cost.__dict__
        del cost_dict["_state"]
        cost_dict["cost"] = 50
        cost_dict["event"] = cost_dict["event_id"]
        del cost_dict["event_id"]

        request = self.client.put(
            reverse("api:events:cost-detail", kwargs={"pk": cost.id}), cost_dict, format="json")

        self.assertEqual(request.status_code, status.HTTP_200_OK)


class CollectionAPITestCase(APITransactionTestCase):

    def setUp(self):
        self.client = APIClient()

        self.event = EventFactory()
        self.collections = CollectionFactory.create_batch(10)
        self.user = ProfileRegistrationDataFactory(user__is_employee=True).user
        self.default_passwd = 'django01'
        self.user.set_password(self.default_passwd)
        self.user.save()

        request_login = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": self.user.username, "password": self.default_passwd}, format="json")

        self.access = request_login.data["access"]
        self.refresh = request_login.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.access)

    def test_collection_list(self):
        request = self.client.get(reverse("api:events:collection-list"))

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 4)

    def test_collection_detail(self):

        collection = self.collections[0]
        request = self.client.get(reverse("api:events:collection-detail", kwargs={"pk": collection.pk}))

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data, CollectionSerializer(collection).data)

    def test_collection_delete(self):
        collection = self.collections[1]
        request = self.client.delete(reverse("api:events:collection-detail", kwargs={"pk": collection.pk}))

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(request.data, None)

    def test_collection_create(self):
        collection_build = CollectionFactory.build().__dict__
        for key in ("_id", "_state"):
            if key in collection_build:
                del collection_build[key]
        collection_build["event"] = self.event.id

        request = self.client.post(reverse("api:events:collection-list"), collection_build, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_collection_edit(self):

        collection = self.collections[2]

        collection_dict = collection.__dict__
        del collection_dict["_state"]
        collection_dict["collection"] = 50
        collection_dict["event"] = collection_dict["event_id"]
        del collection_dict["event_id"]

        request = self.client.put(
            reverse("api:events:collection-detail", kwargs={"pk": collection.id}), collection_dict, format="json")

        self.assertEqual(request.status_code, status.HTTP_200_OK)
