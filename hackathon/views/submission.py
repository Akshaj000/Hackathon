from rest_framework.response import Response
from rest_framework.views import APIView
from hackathon.models import Submission
from user.decorators import handle_refresh


class Submit(APIView):

    @handle_refresh
    def post(self, request):
        data = request.data
        hackathonID = data.get('hackathonID')
        teamID = data.get('teamID')
        file = data.get('file')
        link = data.get('link')
        summary = data.get('summary')
        submission = Submission.objects.create(
            hackathon_id=hackathonID,
            user=request.user
        )
        if teamID:
            submission.team_id = teamID
            submission.save()
        if file:
            submission.file = file
        if link:
            submission.link = link
        if summary:
            submission.summary = summary
        return Response({
            'message': 'Successfully submitted'
        }, status=200)


__all__ = [
    'Submit'
]
