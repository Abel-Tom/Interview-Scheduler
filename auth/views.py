from .serializers import RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from users.models import CustomUser

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class VerifyAPIView(APIView):

    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get(self, request):
        queryset = self.queryset.filter(id=self.request.user.id)
        if (queryset):
            resp = {
                'valid': True,
                'id': queryset[0].id,
                'email': queryset[0].email
            }

        return Response(resp)




class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
