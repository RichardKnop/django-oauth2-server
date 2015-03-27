from django.test import TestCase
from django.core.exceptions import ValidationError

from apps.credentials.models import (
    OAuthUser,
    OAuthClient,
)


class OAuth2UserTestCase(TestCase):
    def test_password_hashing(self):
        user = OAuthUser(
            email='foo@example.com',
            password='password',
        )
        user.save()

        # Check that password is converted to a hash upon saving
        self.assertTrue(user.verify_password('password'))

        # Check that password is not hashed again when its value did not change
        user.save()
        self.assertTrue(user.verify_password('password'))

        # Check that password is hashed again when its value changed
        user.password = '$this_is_my_new_password'
        user.save()
        self.assertFalse(user.verify_password('password'))
        self.assertTrue(user.verify_password('$this_is_my_new_password'))

    def test_email_case_insensivity(self):
        u1 = OAuthUser(
            email='foo@example.com',
            password='password',
        )
        u1.save()

        with self.assertRaises(ValidationError) as context:
            u2 = OAuthUser(
                email='FoO@example.com',
                password='password',
            )
            u2.full_clean()

        self.assertEqual(
            str(context.exception.message_dict['__all__'][0]),
            u'Email not unique',
        )


class OAuth2ClientTestCase(TestCase):
    def test_password_hashing(self):
        client = OAuthClient(
            client_id='fooclient',
            password='password',
        )
        client.save()

        # Check that secret is converted to a hash upon saving
        self.assertTrue(client.verify_password('password'))

        # Check that secret is not hashed again when its value did not change
        client.save()
        self.assertTrue(client.verify_password('password'))

        # Check that secret is hashed again when its value changed
        client.password = '$this_is_my_new_password'
        client.save()
        self.assertFalse(client.verify_password('password'))
        self.assertTrue(client.verify_password('$this_is_my_new_password'))