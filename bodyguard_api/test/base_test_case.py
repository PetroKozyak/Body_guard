import random

from django.core.management import call_command
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


class BaseTestCase(APITestCase):
    USER_DEFAULT_PASSWORD = "adminadmin"
    ROLE_CUSTOMER_ID = 1
    ROLE_FIRM_ID = 2
    ROLE_ID_NOT_EXIST = 10

    def setUp(self):
        call_command('loaddata', 'role_fixtures.json', verbosity=0)


class BaseTestCaseAuthUser(APITestCase):
    OPTION_CAR_VARIANT_YES_ID = 1
    OPTION_CAR_VARIANT_NO_ID = 2
    OPTION_GUN_VARIANT_YES_ID = 3
    OPTION_GUN_VARIANT_NO_ID = 4

    USER_ID_1 = 1
    USER_ID_2 = 2
    USER_ID_3 = 3
    USER_ID_4 = 4
    USER_ID_5_NOT_EXIST = 5

    USER_DEFAULT_PASSWORD = "adminadmin"

    FIRM_ID_1 = 1
    FIRM_NOT_EXIST = 2

    FEEDBACK_ID = 1
    FEEDBACK_NOT_EXIST = 2

    ORDER_ID_1 = 1
    JOB_ID_1 = 1
    JOB_ID_2_SOS = 2
    JOB_ID_3_REGULAR = 3
    JOB_NOT_EXIST = 4

    START_TIME = "2009-02-03 10:10"
    END_TIME = "2010-02-04 10:10"

    BAD_START_TIME = "2020-02-02 10:10"
    BAD_END_TIME = "1966-02-03 10:10"

    COORDINATE = "2026516.265255"
    UPDATE_COORDINATE = "update coordinate"
    BAD_COORDINATE = "56165165165"*100

    COMMENT = "testcomment"
    UPDATE_COMMENT = "changed comment"
    BAD_COMMENT = "bad commment"*100

    GOOD_NUMBER_GUARD = random.randint(1, 10)
    BAD_NUMBER_GUARD = random.randint(11, 99999999)

    GOOD_VARIANTS = [1]
    BAD_VARIANTS = [1, 2]
    VARIANTS_NOT_EXIST = [99]

    TYPE_JOB_REGULAR = 2
    TYPE_JOB_ONE_TYPE = 1
    BAD_JOB_TYPE = 3

    UPDATE_TITLE = "update test title"
    BAD_TITLE = "update test title"*100

    NEW_NAME_FIRM = "New name"
    NEW_BAD_NAME_FIRM = "New name"*100

    def setUp(self):
        call_command('loaddata', 'role_fixtures.json', verbosity=0)
        call_command('loaddata', 'user_fixtures.json', verbosity=0)
        call_command('loaddata', 'user_profile_fixtures.json', verbosity=0)
        call_command('loaddata', 'option_fixtures.json', verbosity=0)
        call_command('loaddata', 'variant_option_fixtures.json', verbosity=0)
        call_command('loaddata', 'firm_fixtures.json', verbosity=0)
        call_command('loaddata', 'feedback_fixtures.json', verbosity=0)
        call_command('loaddata', 'job_fixtures.json', verbosity=0)
        call_command('loaddata', 'order_fixtures.json', verbosity=0)

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
