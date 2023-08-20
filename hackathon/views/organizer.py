from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from hackathon.decorators import resolve_hackathon
from user.authentication import CookieTokenAuthentication
from hackathon.serializers import OrganiserInputSerializer, HackathonOutputSerializer
from user.decorators import handle_refresh
from user.models import User
from hackathon.models import Organiser


class AddOrganizerView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrganiserInputSerializer

    @handle_refresh
    @resolve_hackathon("admin")
    def post(self, request, *args, **kwargs):
        data = request.data
        hackathon = self.hackathon
        organisers = data.get('organisers')
        if not organisers:
            return Response({
                'error': {
                    'code': "ORGANISERS_REQUIRED",
                    'message': 'Organisers are required'
                },
            }, status=400)
        if User.objects.filter(id__in=[organiser.get('userID') for organiser in data.get('organisers')]).count() != len(data.get('organisers')):
            return Response({
                'error': {
                    'code': 'INVALID_USER',
                    'message': 'Invalid user ID'
                }
            }, status=400)
        if Organiser.objects.filter(user_id__in=[organiser.get('userID') for organiser in data.get('organisers')], hackathon=hackathon).count() != 0:
            return Response({
                'error': {
                    'code': 'ORGANISER_EXISTS',
                    'message': 'Organiser already exists'
                }
            }, status=400)
        for organiser in data.get('organisers'):
            Organiser.objects.create(
                user_id=organiser.get('userID'),
                hackathon=hackathon,
                access=organiser.get('access')
            )
        return Response(HackathonOutputSerializer(hackathon).data, status=200)


class RemoveOrganizerView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrganiserInputSerializer

    @handle_refresh
    @resolve_hackathon("admin")
    def post(self, request, *args, **kwargs):
        data = request.data
        hackathon = self.hackathon
        organisers = data.get('organisers')
        if not organisers:
            return Response({
                'error': {
                    'code': "ORGANISERS_REQUIRED",
                    'message': 'Organisers are required'
                },
            }, status=400)
        if User.objects.filter(id__in=[organiser.get('userID') for organiser in data.get('organisers')]).count() != len(data.get('organisers')):
            return Response({
                'error': {
                    'code': 'INVALID_USER',
                    'message': 'Invalid user ID'
                }
            }, status=400)
        if Organiser.objects.filter(user_id__in=[organiser.get('userID') for organiser in data.get('organisers')], hackathon=hackathon).count() != len(data.get('organisers')):
            return Response({
                'error': {
                    'code': 'ORGANISER_DOES_NOT_EXIST',
                    'message': 'Organiser does not exist'
                }
            }, status=400)
        for organiser in data.get('organisers'):
            Organiser.objects.filter(
                user_id=organiser.get('userID'),
                hackathon=hackathon,
            ).delete()
        return Response(HackathonOutputSerializer(hackathon).data, status=200)


class OrganizersView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrganiserInputSerializer

    @handle_refresh
    @resolve_hackathon("viewer")
    def get(self, request, *args, **kwargs):
        hackathon = self.hackathon
        organisers = Organiser.objects.filter(hackathon=hackathon)
        return Response({
            'organisers': OrganiserInputSerializer(organisers, many=True).data
        }, status=200)


__all__ = [
    'AddOrganizerView',
    'RemoveOrganizerView',
    'OrganizersView'
]

