from rest_framework.serializers import ModelSerializer, SerializerMethodField
from store.models import Store
from address.api.serializers import AddressSerializer


class StoreSerializer(ModelSerializer):
    address = AddressSerializer(required=False)
    mobile = SerializerMethodField(required=False)

    class Meta:
        model = Store
        fields = ('id', 'name', 'about', 'owner', 'icon', 'icon', 'banner', 'address','categories', 'num_sales', 'mobile')
        read_only_fields = ['categories']

    def get_mobile(self, object):
        return object.owner.mobile
