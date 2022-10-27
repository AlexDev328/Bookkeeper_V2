from django.contrib.auth.models import User
from django.test import TestCase
from booking.models import Currency, Account, Transaction, Cost, Convertation
from user_profile.models import Profile


class ProfileTestCase(TestCase):

    def test_user_profile_create_with_currency(self):
        currency = Currency.objects.create(name="test", sign="t")
        user = User.objects.create_user(username="testuser", email='test@user.com', password='123456')
        profile = Profile.objects.first()

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.default_currency, currency)

    def test_user_profile_create_without_currency(self):
        user = User.objects.create_user(username="testuser", email='test@user.com', password='123456')
        profile = Profile.objects.first()

        self.assertEqual(profile.user, user)
        self.assertIsNone(profile.default_currency)
