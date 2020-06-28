from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from .serializers import StoreSerializer
from store.models import Store
from rest_framework import filters


class StoreList(ListAPIView, ListModelMixin):
    serializer_class = StoreSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'about']

    def get_queryset(self):
        queryset = Store.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)

