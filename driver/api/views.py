from .serializers import DriverSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from driver.models import Driver
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status


class DriverList(ListCreateAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()

    # list ✓
    # create
    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            mobile = self.request.data.get('mobile', None)
            fullname = self.request.data.get('fullname', None)
            if mobile:
                try:
                    user = User.objects.get(mobile=mobile)
                except User.DoesNotExist:
                    temp_email = "doorpay987654321@doorpay.com"
                    user = User(mobile=mobile, email=temp_email, username=mobile, password="nc9ehr4cx3cxf3y4nc3r")
                    if fullname:
                        user.fullname = fullname
                    user.save()
                driver = Driver(user=user)
                driver.save()
                serializer = self.serializer_class(driver, context={'request': request})
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response({'msg': 'Please provide mobile number'}, status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DriverDetail(RetrieveUpdateDestroyAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    lookup_field = 'id'

    # get ✓
    # put
    def put(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            fullname = self.request.data.get('fullname', None)
            is_active = self.request.data.get('is_active', None)
            instance = self.get_object()
            if fullname:
                user = instance.user
                user.fullname = fullname
                user.save()
            if is_active:
                instance.is_active = is_active
                instance.save()
            serializer = self.serializer_class(instance, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.destroy(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
