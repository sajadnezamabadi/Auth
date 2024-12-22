from django.urls import path
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
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
    
    #swagger
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
