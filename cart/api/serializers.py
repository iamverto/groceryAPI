from rest_framework.serializers import ModelSerializer, SerializerMethodField
from cart.models import Cart, CartItem
from product.api.serializers import ProductSerializer


class CartItemSerializer(ModelSerializer):

    product_title = SerializerMethodField(read_only=True)
    product_price = SerializerMethodField(read_only=True)
    product_featured_image = SerializerMethodField(read_only=True)
    product_store_name = SerializerMethodField(read_only=True)
    is_product_active = SerializerMethodField(read_only=True)
    store=SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity', 'product_title',
                  'product_price', 'product_featured_image',
                  'product_store_name', 'is_product_active','store')

    def get_product_title(self, object):
        return object.product.title

    def get_product_price(self, object):
        return object.product.price

    def get_product_featured_image(self, object):
        request = self.context['request']
        feature_image = object.product.get_featured_image()
        if feature_image:
            return request.build_absolute_uri(feature_image)
        return None

    def get_product_store_name(self, object):
        return object.product.get_store_name()

    def get_is_product_active(self, object):
        return object.product.is_active

    def get_store(self, object):
        return object.product.store.id
