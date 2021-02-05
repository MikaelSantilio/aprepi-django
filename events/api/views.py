from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.conf import settings
from core import mercadopago
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from users.models import Benefactor
from events.models import EventDonation, Event, Cost, Collection
from events.api.serializers import (
    EventSerializer,
    EventHATEOASerializer,
    CostSerializer,
    CollectionSerializer,
    EventDonationCreateSerializer,
    EventDonationSerializer,
)

from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_employee)


class IsBenefactor(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_benefactor)


class ListPaginatedMixin():

    def custom_paginated_queryset(self, request, Serializer):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = Serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = Serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class CostListCreateAPIView(ListCreateAPIView):
    queryset = Cost.objects.all()
    serializer_class = CostSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['event']
    ordering_fields = ['cost']

    def check_create_permissions(self, request):

        permission = [IsAdminUser | IsEmployee][0]()
        if not permission.has_permission(request, self):
            self.permission_denied(
                request,
                message=getattr(permission, 'message', None),
                code=getattr(permission, 'code', None)
            )

    def post(self, request, *args, **kwargs):
        self.check_create_permissions(request)
        return self.create(request, *args, **kwargs)


class CostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Cost.objects.all()
    serializer_class = CostSerializer
    permission_classes = [IsAdminUser | IsEmployee]


class CollectionListCreateAPIView(ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['event']
    ordering_fields = ['collection']

    def check_create_permissions(self, request):

        permission = [IsAdminUser | IsEmployee][0]()
        if not permission.has_permission(request, self):
            self.permission_denied(
                request,
                message=getattr(permission, 'message', None),
                code=getattr(permission, 'code', None)
            )

    def post(self, request, *args, **kwargs):
        self.check_create_permissions(request)
        return self.create(request, *args, **kwargs)


class CollectionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminUser | IsEmployee]


class EventViewSet(ListPaginatedMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-end_date')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = []
    ordering_fields = ['end_date', 'start_date', 'event_name']

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser | IsEmployee]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return self.custom_paginated_queryset(request, EventHATEOASerializer)

    # def retrieve(self, request, pk=None):
    #     obj = get_object_or_404(Car, pk=pk)
    #     serializer = CarDetailSerializer(obj)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
