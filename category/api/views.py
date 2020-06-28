from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from .serializers import CategorySerializer
from category.models import Category


class CategoryList(ListAPIView, ListModelMixin):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)