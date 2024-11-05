from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Custom User model
class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    confirmation_sent_at = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    failed_login_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)

    def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
        self.lockout_until = None
        self.save()

    def increment_failed_login_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lockout_until = timezone.now() + timezone.timedelta(minutes=5)
        self.save()

    @property
    def comments_count(self):
        return self.comments.count()
