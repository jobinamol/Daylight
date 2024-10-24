from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # Set username to email prefix
        email = data.get('email')
        if email:
            username = email.split('@')[0]
            i = 1
            while User.objects.filter(username=username).exists():
                username = f"{username}{i}"
                i += 1
            user.username = username
        
        # Optionally, set other fields if available
        if 'name' in data:
            name_parts = data['name'].split(' ', 1)
            user.first_name = name_parts[0]
            if len(name_parts) > 1:
                user.last_name = name_parts[1]
        
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # Perform any additional actions after saving the user
        # For example, you could create a profile for the user here
        
        return user