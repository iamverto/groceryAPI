from rest_framework.serializers import ModelSerializer, SerializerMethodField
from driver.models import Driver
from accounts.api.serializers import UserSerializer

class DriverSerializer(ModelSerializer):
    fullname = SerializerMethodField(read_only=True)
    mobile = SerializerMethodField(read_only=True)
    class Meta:
        model = Driver
        fields = ('id', 'user', 'fullname', 'mobile', 'is_active')


    def get_fullname(self, instance):
        if instance.user is not None:
            return instance.user.fullname
        return None

    def get_mobile(self, instance):
        if instance.user is not None:
            return instance.user.mobile
        return None