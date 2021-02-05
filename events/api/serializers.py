from django.urls import reverse
from rest_framework import serializers

from events import models


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = '__all__'


class CostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cost
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Collection
        fields = '__all__'


class EventDonationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventDonation
        fields = '__all__'


class EventDonationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventDonation
        fields = ('donated_value', 'event')


class EventHATEOASerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = ('id', 'event_name', 'start_date', 'end_date', 'links')

    def get_links(self, obj):
        data = []

        request = self.context['request']

        if request.user.is_authenticated:
            data.append(
                {
                    "type": "GET",
                    "rel": "self",
                    "uri": request.build_absolute_uri(
                        reverse("api:events:events-detail", kwargs={'pk': obj.id}))
                }
            )

            if request.user.is_employee or request.user.is_superuser:
                data += [
                    {
                        "type": "GET",
                        "rel": "evento_despesas",
                        "uri": request.build_absolute_uri(f'{reverse("api:events:cost-list")}?event={obj.id}')
                    },
                    {
                        "type": "GET",
                        "rel": "evento_arrecadacao",
                        "uri": request.build_absolute_uri(f'{reverse("api:events:collection-list")}?event={obj.id}')
                    },
                    {
                        "type": "PUT",
                        "rel": "evento_atualizacao",
                        "uri": request.build_absolute_uri(reverse("api:events:events-detail", kwargs={'pk': obj.id}))
                    },
                    {
                        "type": "DELETE",
                        "rel": "evento_exclusao",
                        "uri": request.build_absolute_uri(reverse("api:events:events-detail", kwargs={'pk': obj.id}))
                    }
                ]

        return data
