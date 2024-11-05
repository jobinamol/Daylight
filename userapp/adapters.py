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
        
        # Set emailid field
        user.emailid = email
        
        # Optionally, set other fields if available
        if 'name' in data:
            user.name = data['name']  # Assuming your UserDB model has a 'name' field
        
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # Ensure emailid is set
        if not user.emailid:
            user.emailid = sociallogin.account.extra_data.get('email', '')
        
        # Set other fields from sociallogin data
        user.name = sociallogin.account.extra_data.get('name', '')
        
        # Save the user again to ensure all fields are updated
        user.save()
        
        return user