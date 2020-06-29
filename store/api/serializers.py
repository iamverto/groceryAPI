from rest_framework.serializers import ModelSerializer
from store.models import Store
from address.api.serializers import AddressSerializer


class StoreSerializer(ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Store
        fields = ('id', 'name', 'about', 'owner', 'icon', 'icon', 'banner', 'address','categories', 'num_sales')
