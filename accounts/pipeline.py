from django.contrib.auth import logout
from accounts.custom_auth import custom_logout 
def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    print("\n\n\n    SSSSSSSSSSSSSSScccccccccccccccccccccc : ",social)
    
    if social:
        if user and social.user != user:
            logout(backend.strategy.request)
        elif not user:
            user = social.user
    print("\n\n\n    SSSSSSSSSSSSSSScccccccccccccccccccccc : ",user)        
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}