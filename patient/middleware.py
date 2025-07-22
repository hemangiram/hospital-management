# middleware.py

from django.contrib.sessions.models import Session
from django.utils.deprecation import MiddlewareMixin
from patient.models import UserProfile  # adjust import based on your project structure

class OneSessionPerUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            print(f"Processing request for user: {request.user.username}")
            current_session_key = request.session.session_key

            # 1. Attach role to request
            try:
                request.role = request.user.userprofile.role.name.lower()
                print(f"Role attached: {request.role}")
            except UserProfile.DoesNotExist:
                request.role = None
                print(f" No UserProfile found for user: {request.user.username}")

            # 2. Limit to single session per user
            user_sessions = Session.objects.filter(expire_date__gte=request.session.get_expiry_date())
            for session in user_sessions:
                data = session.get_decoded()
                if str(data.get('_auth_user_id')) == str(request.user.id) and session.session_key != current_session_key:
                    print(f" Deleting old session: {session.session_key}")
                    session.delete()



