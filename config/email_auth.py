from django.contrib.auth.models import User

# todo enable
class EmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        # check if the user is active and if the password is correct -> return user
        if user.check_password(password):
            return user
        
        return None

    # method to get the user from the DB
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        
        except User.DoesNotExist:
            return None
        