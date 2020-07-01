import jwt
import pyotp
from django.contrib.auth import authenticate
from django.contrib.auth import user_logged_in
from rest_framework_jwt.utils import jwt_payload_handler

from address.models import Address
from grocery_app import settings
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User

from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin

from address.api.serializers import AddressSerializer

from rest_framework_jwt.settings import api_settings
from twilio.rest import Client as TwilioClient

twilio_phone = "+18125788624"
client = TwilioClient('ACc2b22b8a563f703840d33757384ccc51', "9661ad9e648c14caa100c07e13c89972")


def get_token(obj):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(obj)
    token = jwt_encode_handler(payload)
    print(obj, payload, token)
    return token


def get_user(token):
    jwt_get_user_from_token = api_settings.JWT_DECODE_HANDLER
    return jwt_get_user_from_token(token)


# login
# create user if not available + send OTP
@api_view(['get'])
def user(request):
    user = request.user
    token = get_token(user)
    serializer = UserSerializer(user, context={'request':request})
    data = serializer.data
    data['token'] = token
    return Response(data, status=status.HTTP_200_OK)


@api_view(['post'])
@permission_classes([AllowAny])
def login(request):
    mobile = request.data.get('mobile', None)
    if mobile:
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            temp_email = "doorpay987654321@doorpay.com"
            user = User(mobile=mobile, email=temp_email, username=mobile, password="nc9ehr4cx3cxf3y4nc3r")
            user.save()
        # generate OTP
        time_otp = pyotp.TOTP(user.key, interval=900)
        time_otp = time_otp.now()
        print(time_otp)
        # send sms code
        # client.messages.create(
        #     body="Your FuseGrocer verification code is " + time_otp,
        #     from_=twilio_phone,
        #     to="+91" + user.mobile
        # )
        return Response({}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
@permission_classes([AllowAny])
def verify_otp(request):
    mobile = request.data.get('mobile', None)
    otp = request.data.get('otp', None)
    try:
        user = User.objects.get(mobile=mobile)
    except User.DoesNotExist:
        user = None
    if otp and user:
        print(otp, user)
        t = pyotp.TOTP(user.key, interval=900)
        is_verified = t.verify(otp)
        print(is_verified)
        if is_verified:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                serializer = UserSerializer(user, context={'request': request})
                data = serializer.data
                data['token'] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(data, status=status.HTTP_200_OK)
            except Exception as e:
                raise e

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    print("jihj")
    if username and password:
        print(username, password)
        try:
            user = authenticate(username=username, password=password)
        except User.DoesNotExist:
            return Response({'msg': 'err'}, status.HTTP_401_UNAUTHORIZED)
        user_data = {
            'id': user.id,
            'username': user.username,
            'token':get_token(user)
        }
        return Response(user_data, status.HTTP_200_OK)
    else:
        return Response({},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_addresses(request):
    addresses = request.user.addresses.all()
    serializer = AddressSerializer(addresses, many=True, context={'request':request})
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def get_address(request, id):
    try:
        address = request.user.addresses.get(id=id)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AddressSerializer(address, context={'request': request})
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def update_address(request, id):
    try:
        address = request.user.addresses.get(id=id)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AddressSerializer(address, request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_address(request):
    serializer = AddressSerializer(data=request.data, context={'request':request})
    if serializer.is_valid():
        serializer.save()
        request.user.addresses.add(serializer.instance)
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def delete_address(request, id):
    try:
        address = request.user.addresses.get(id=id)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    address.delete()
    return Response(status=status.HTTP_200_OK)


class UserList(ListAPIView, ListModelMixin):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
