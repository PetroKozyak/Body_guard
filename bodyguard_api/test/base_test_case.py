from django.core.management import call_command
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


class BaseTestCase(APITestCase):

    ROLE_CUSTOMER_ID = 1
    ROLE_FIRM_ID = 2

    def setUp(self):
        call_command('loaddata', 'role_fixtures.json', verbosity=0)


class BaseTestCaseAuthUser(APITestCase):
    USER_ID_1 = 1
    USER_ID_2 = 2
    USER_ID_3 = 3
    USER_ID_4_NOT_EXIST = 4

    USER_DEFAULT_PASSWORD = "adminadmin"



    def setUp(self):
        call_command('loaddata', 'role_fixtures.json', verbosity=0)
        call_command('loaddata', 'user_fixtures.json', verbosity=0)
        call_command('loaddata', 'user_profile_fixtures.json', verbosity=0)
        call_command('loaddata', 'option_fixtures.json', verbosity=0)
        call_command('loaddata', 'variant_option_fixtures.json', verbosity=0)


    def before_test(self, user_id):
        self.user = User.objects.filter(pk=user_id).first()
        if self.user:
            resp = self.client.post(reverse('get-token'),
                                    {'username': self.user.username, 'password': self.USER_DEFAULT_PASSWORD},
                                    format='json')
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertTrue('token' in resp.data)
            self.token = resp.data.get('token')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        else:
            self.token = None
            self.client.credentials(HTTP_AUTHORIZATION='JWT')
        return self.user
