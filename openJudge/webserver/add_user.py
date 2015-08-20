import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    from question.models import Profile
    import django
    django.setup()
    p = Profile()
    p.username=input('Username:')
    p.set_password(input('Password:'))
    p.save()
