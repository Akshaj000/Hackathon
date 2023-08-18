from django.contrib import admin
from django.urls import path

from user.views import UserRegisterView, UserLoginView, UserLogoutView, ProfileView, UpdateProfileView, DeleteAccountView

urlpatterns = [
    path('admin/', admin.site.urls),

    # User
    path('api/signup/', UserRegisterView.as_view()),
    path('api/login/', UserLoginView.as_view()),
    path('api/logout/', UserLogoutView.as_view()),
    path('api/profile/', ProfileView.as_view()),
    path('api/profile/update/', UpdateProfileView.as_view()),
    path('api/profile/delete/', DeleteAccountView.as_view()),

]
