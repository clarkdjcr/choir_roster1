from django.utils import timezone
from .models import ChoirMember

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                choir_member = request.user.choirmember
                choir_member.update_online_status(True)
            except:
                pass
        response = self.get_response(request)
        return response 