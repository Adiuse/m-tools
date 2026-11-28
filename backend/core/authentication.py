from rest_framework.authentication import SessionAuthentication


class WorkbenchSessionAuthentication(SessionAuthentication):
    def authenticate_header(self, request):
        return "Session"
