from django.contrib import admin
from django.urls import path

from user.views import (
    UserRegisterView, UserLoginView, UserLogoutView, UsersView,
    ProfileView, UpdateProfileView, DeleteAccountView, UserView
)
from team.views import (
    CreateTeamView, UpdateTeamView, AddTeamMembersView, RemoveTeamMembersView,
    LeaveTeamView, TeamView, TeamsView,
    TransferOwnershipView, DeleteTeamView
)
from hackathon.views import (
    PublishHackathonView, UpdateEvaluationView, DeleteHackathonView,
    EvaluateSubmissionView, AddOrganizerView, RemoveOrganizerView, UpdateHackathonView,
    CreateSubmissionView, CreateRegistrationView, HackathonView, HackathonListView,
    MyRegistrationsView, MySubmissionsView, OrganizersView, RegistrationsView,
    SubmissionsView
)

urlpatterns = [
    path('api/admin/', admin.site.urls),

    # User
    path('api/user/signup/', UserRegisterView.as_view()),
    path('api/user/login/', UserLoginView.as_view()),
    path('api/user/logout/', UserLogoutView.as_view()),
    path('api/user/profile/', ProfileView.as_view()),
    path('api/user/profile/update/', UpdateProfileView.as_view()),
    path('api/user/delete/', DeleteAccountView.as_view()),
    path('api/user/', UserView.as_view()),
    path('api/users/', UsersView.as_view()),

    # Team
    path('api/team/create/', CreateTeamView.as_view()),
    path('api/team/update/', UpdateTeamView.as_view()),
    path('api/team/delete/', DeleteTeamView.as_view()),
    path('api/team/add-members/', AddTeamMembersView.as_view()),
    path('api/team/remove-members/', RemoveTeamMembersView.as_view()),
    path('api/team/leave/', LeaveTeamView.as_view()),
    path('api/team/transfer-ownership/', TransferOwnershipView.as_view()),
    path('api/team/', TeamView.as_view()),
    path('api/teams/', TeamsView.as_view()),


    # Hackathon
    path('api/hackathon/publish/', PublishHackathonView.as_view()),
    path('api/hackathon/update/', UpdateHackathonView.as_view()),
    path('api/hackathon/delete/', DeleteHackathonView.as_view()),
    path('api/hackathon/evaluate/', EvaluateSubmissionView.as_view()),
    path('api/hackathon/update-evaluation/', UpdateEvaluationView.as_view()),
    path('api/hackathon/add-organizer/', AddOrganizerView.as_view()),
    path('api/hackathon/remove-organizer/', RemoveOrganizerView.as_view()),
    path('api/hackathon/register/', CreateRegistrationView.as_view()),
    path('api/hackathon/submit/', CreateSubmissionView.as_view()),
    path('api/hackathon/', HackathonView.as_view()),
    path('api/hackathons/', HackathonListView.as_view()),
    path('api/hackathon/registrations/', RegistrationsView.as_view()),
    path('api/hackathon/submissions/', SubmissionsView.as_view()),
    path('api/hackathon/my-registrations/', MyRegistrationsView.as_view()),
    path('api/hackathon/my-submissions/', MySubmissionsView.as_view()),
    path('api/hackathon/organizers/', OrganizersView.as_view()),
]
