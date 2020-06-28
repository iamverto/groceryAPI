from rest_framework.serializers import ModelSerializer
from address.models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'city', 'pincode', 'street')
