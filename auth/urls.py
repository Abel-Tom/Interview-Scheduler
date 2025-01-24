from django.urls import path
from auth.views import RegisterView, LogoutView, LogoutAllView, VerifyAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/verify/', VerifyAPIView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
]

