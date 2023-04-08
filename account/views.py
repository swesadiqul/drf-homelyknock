from .models import User
from .serializers import *
from account.renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import *
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
User = get_user_model()
from rest_framework.parsers import MultiPartParser, FormParser
import pyotp
import datetime
from .otp import send_otp_via_email
from rest_framework import viewsets
from django.utils import timezone
from django.db.models import Q
from profile_settings.models import Profile
from profile_settings.serializers import ProfileSerializer




def generate_otp():
    # Generate a random secret key
    secret = pyotp.random_base32()

    # Create an OTP object
    totp = pyotp.TOTP(secret, digits=4)

    # Generate the OTP
    otp = totp.now()

    return secret, otp



# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class RegistrationAPIView(APIView):
    # def post(self, request):
    #     email = request.data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         return Response({'message': 'User with this email already exists.'}, status=status.HTTP_409_CONFLICT)
    #     serializer = RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'User successfully registered.'}, status=status.HTTP_200_OK)
    #     else:
    #          return Response({'message': 'Invalid credentials.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        # Create a new User object
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Profile object for the User
        profile = Profile(user=user)
        profile.save()

        # Return a response with the created User and Profile objects
        user_serializer = RegistrationSerializer(user)
        profile_serializer = ProfileSerializer(profile)
        return Response({'user': user_serializer.data, 'profile': profile_serializer.data}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            data = {'message': 'Email and password are required fields.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                token = get_tokens_for_user(user)
                serializer = RegistrationSerializer(user)
                access_token = token['access']
                data = {
                    'token': access_token,
                    'message': 'User successfully logged in.',
                    'user': serializer.data
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {'message': 'Invalid email or password.'}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            data = {'message': str(e)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out."})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response({'status': 'Password changed successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordOTPAPIView(APIView):
    serializer_class = ResetPasswordOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_or_email = serializer.validated_data['phone_or_email']
        media = serializer.validated_data['media']

        if media == 'email':
            user = User.objects.filter(email=phone_or_email).first()
            if user:
                # Generate and save OTP for the user
                otp_secret, otp = generate_otp()
                user.otp_secret = otp_secret
                user.otp = otp
                user.otp_expire_time = timezone.now() + datetime.timedelta(minutes=1)
                user.save()

                # Send OTP via email
                send_otp_via_email(user.email, otp)

                return Response({'success': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)

        elif media == 'phone':
            user = User.objects.filter(phone_number=phone_or_email).first()
            if user:
                # Generate and save OTP for the user
                otp_secret, otp = generate_otp()
                user.otp_secret = otp_secret
                user.otp = otp
                user.otp_expire_time = timezone.now() + datetime.timedelta(minutes=1)
                user.save()

                # Send OTP via SMS (using Twilio or other service)
                # send_otp_via_sms(user.phone_number, otp)

                return Response({'success': 'OTP has been sent to your phone.'}, status=status.HTTP_200_OK)

        # raise serializers.ValidationError('User not found.')
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class VerifyOTPAPIView(APIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_or_email = serializer.validated_data['phone_or_email']
        otp = serializer.validated_data['otp']

        user = User.objects.filter(Q(email=phone_or_email) | Q(phone_number=phone_or_email)).first()
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp != otp:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.otp_expire_time < timezone.now():
            return Response({'error': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # If OTP is valid and not expired, reset the password
        # Reset the OTP and OTP expire time
        user.otp = None
        user.otp_expire_time = None
        user.save()

        return Response({'success': 'OTP has been verified.'}, status=status.HTTP_200_OK)



class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_or_email = serializer.validated_data['phone_or_email']
        password = serializer.validated_data['password']

        user = User.objects.filter(Q(email=phone_or_email) | Q(phone_number=phone_or_email)).first()
        if not user:
             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()

        return Response({'success': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


class ServiceList(generics.ListCreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


# class LocationList(generics.ListCreateAPIView):
#     queryset = ServiceLocation.objects.all()
#     serializer_class = ServiceLocationSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class LocationList(generics.ListCreateAPIView):
    serializer_class = ServiceLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the user based on their information
        email = self.kwargs.get('email')
        # user = get_object_or_404(User, email=email)
        user = self.request.user

        # Filter the queryset by the retrieved user
        return ServiceLocation.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ServiceLocation.objects.all()
    serializer_class = ServiceLocationSerializer


class SMSTemplateList(generics.ListCreateAPIView):
    queryset = SMSTemplate.objects.all()
    serializer_class = SMSTemplateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SMSTemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SMSTemplate.objects.all()
    serializer_class = SMSTemplateSerializer
    permission_classes = [IsAuthenticated]


class EmailTemplateList(generics.ListCreateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmailTemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    
class OneClickResponseList(APIView):
    def get(self, request, id=None, format=None):
        id=id
        if id is not None:
            query = OneClickResponse.objects.filter(user = request.user,id=id)
            serializer = OneClickResponseSerializer(query,many=True)
            return Response(serializer.data)
        query = OneClickResponse.objects.filter(user = request.user)
        serializer = OneClickResponseSerializer(query,many=True)
        return Response(serializer.data) 
    

    def put(self, request, id, format=None):
        id = id
        query = OneClickResponse.objects.get(id=id)
        serializer = OneClickResponseSerializer(query, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.user = request.user
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    parser_classes = (MultiPartParser, FormParser,)
    # permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
