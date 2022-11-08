from django.urls import path
from authentication.views.myobtaintokenpairview import MyObtainTokenPairView
from authentication.views.registerview import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegisterView.as_view(), name='auth-signup')
]
