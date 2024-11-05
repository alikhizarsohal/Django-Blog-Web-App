from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import \
    text_type  # Import `text_type` from the standalone `six` package


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(
                user.pk) +
            text_type(timestamp) +
            text_type(
                user.email_confirmed))


account_activation_token = TokenGenerator()
