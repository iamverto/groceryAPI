from rest_framework.serializers import ModelSerializer, SerializerMethodField
from order.models import Order, OrderItem
from address.api.serializers import AddressSerializer
from accounts.api.serializers import UserSerializer
from store.api.serializers import StoreSerializer


class OrderItemSerializer(ModelSerializer):

    product_title = SerializerMethodField(read_only=True)
    product_price = SerializerMethodField(read_only=True)
    product_featured_image = SerializerMethodField(read_only=True)
    product_store_name = SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'quantity', 'product_title',
                  'product_price', 'product_featured_image',
                  'product_store_name')

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


class OrderSerializer(ModelSerializer):
    address = AddressSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    # shipping details

    class Meta:
        model = Order
        fields = ('id','user', 'store', 'order_date', 'amount', 'address', 'items', 'status')
