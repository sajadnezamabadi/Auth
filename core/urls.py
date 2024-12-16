from django.urls import path
from .views import *

#--------------------------------

#/api/""
urlpatterns = [
    path("register", RegisterApiView.as_view(), name=""),
    path("login", LoginApiView.as_view(), name=""),
    # path('two-factor', TwoFactorAPIView.as_view()),
    # path('google-auth', GoogleAuthAPIView.as_view()),
    path("user", UserApiView.as_view(), name=""),
    path("refresh", RefreshApiView.as_view(), name=""),
    path("logout", LogoutApiview.as_view(), name=""),
    path("forgot", forgotApiView.as_view(), name=""),
    path("reset", ResetApiView.as_view(), name=""),
]
