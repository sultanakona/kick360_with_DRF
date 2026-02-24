from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.exceptions import APIResponse

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # We are not doing token blacklisting for now, 
        # so simply returning success so the client can drop the token.
        return APIResponse(message="Logout successful.")
