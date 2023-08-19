from django.contrib import admin
from django.urls import path

from user.views import (
    UserRegisterView, UserLoginView, UserLogoutView, ProfileView, UpdateProfileView, DeleteAccountView
)
from team.views import (
    CreateTeamView, UpdateTeamView, AddTeamMembersView, RemoveTeamMembersView, LeaveTeamView,
    TransferOwnershipView, DeleteTeamView
)
from hackathon.views import CreateHackathonView

urlpatterns = [
    path('admin/', admin.site.urls),

    # User
    path('api/user/signup/', UserRegisterView.as_view()),
    path('api/user/login/', UserLoginView.as_view()),
    path('api/user/logout/', UserLogoutView.as_view()),
    path('api/user/profile/', ProfileView.as_view()),
    path('api/user/profile/update/', UpdateProfileView.as_view()),
    path('api/user/delete/', DeleteAccountView.as_view()),

    # Team
    path('api/team/create/', CreateTeamView.as_view()),
    path('api/team/update/', UpdateTeamView.as_view()),
    path('api/team/delete/', DeleteTeamView.as_view()),
    path('api/team/add-members/', AddTeamMembersView.as_view()),
    path('api/team/remove-members/', RemoveTeamMembersView.as_view()),
    path('api/team/leave/', LeaveTeamView.as_view()),
    path('api/team/transfer-ownership/', TransferOwnershipView.as_view()),


    # Hackathon
    path('api/hackathon/create/', CreateHackathonView.as_view()),
]
