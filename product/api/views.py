from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from product.models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from rest_framework import filters
from django.shortcuts import get_object_or_404


class ProductListCreateAPIView(ListCreateAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'is_active', 'num_sales']

    def get_queryset(self):
        """ Filters : STORE|CATEGORY """
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        store = self.request.query_params.get('store', None)
        is_active = self.request.query_params.get('is_active', None)

        if category:
            queryset = queryset.filter(categories__in=category)
        if store:
            queryset = queryset.filter(store=store)
        if is_active:
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request)

    # only for admin
    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            print(request.data)
            return self.create(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProductRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView, RetrieveModelMixin, UpdateModelMixin,
                                         DestroyModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)

    def put(self, request, *args, **kwargs):
        pass

    # only for admin
    def patch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.partial_update(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # only for admin
    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.destroy(self, request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_image(request):
    # data : product, pic
    serializer = ProductImageSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # print(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_image(request, id):
    instance = get_object_or_404(ProductImage, id=id)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
