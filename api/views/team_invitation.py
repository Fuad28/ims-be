from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import TeamInvitation
from api.permissions import TeamInvitationPermission
from api.utils.mail import send_mail

from api.models import TeamInvitation
from api.serializers.team_invitation import TeamInvitationSerializer



class TeamInvitationView(APIView):
    permission_classes= [TeamInvitationPermission]

    def post(self, request, *args, **kwargs):
        serializer= TeamInvitationSerializer(data= request.data)
        serializer.is_valid(raise_exception= True)

        team_invitation_emails= TeamInvitation.objects.filter(
            business= request.user.business, is_registered= False
            ).values_list("email", flat= True)
        
        invitees= [
            data for data in serializer.validated_data.get("data") \
            if data["email"] not in team_invitation_emails]
    
        
        team_members= [
            TeamInvitation(
                email= data["email"],
                role= data["role"],
                business= request.user.business
            )

            for data in invitees
            
        ]
        
        if len(team_members):
            TeamInvitation.objects.bulk_create(team_members, ignore_conflicts= True)

            send_mail(
                subject= "IMS Invite", 
                recipients= [data["email"] for data in invitees], 
                template= "emails/team_invitation.html", 
                data= {"frontend_signup_url": settings.FRONTEND_SIGNUP_URL})

            return Response({"detail": "Invites sent."}, status= status.HTTP_200_OK)

        return Response({"detail": "Invites sent to user already."}, status= status.HTTP_400_BAD_REQUEST)