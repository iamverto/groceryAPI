from rest_framework.serializers import ModelSerializer, SerializerMethodField
from product.models import Product, ProductImage


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'pic', 'is_featured')


class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    store_name = SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description','price', 'categories', 'is_active', 'store', 'store_name', 'images', 'num_sales')

    def get_store_name(self, product):
        return product.get_store_name()