from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCase


class UserCreateAPIViewTestCase(BaseTestCase):
    url = reverse("users-list")

    createuser = lambda: (
        ({"username": 'user_name1',
          "first_name": BaseTestCase.USER_NAME,
          "last_name": BaseTestCase.USER_LAST_NAME,
          "email": 'user1@admin.com',
          "password": BaseTestCase.USER_DEFAULT_PASSWORD,
          "role": BaseTestCase.ROLE_CUSTOMER_ID,
          }, 2, 201),

        ({"username": 'user_name2',
          "first_name": BaseTestCase.USER_NAME,
          "last_name": BaseTestCase.USER_LAST_NAME,
          "email": 'user2@admin.com',
          "password": BaseTestCase.USER_DEFAULT_PASSWORD,
          "role": BaseTestCase.ROLE_FIRM_ID,
          }, 2, 201),

        ({"username": 'user_name2' * 100,
          "first_name": BaseTestCase.USER_NAME,
          "last_name": BaseTestCase.USER_LAST_NAME,
          "email": 'user2@admin.com',
          "password": BaseTestCase.USER_DEFAULT_PASSWORD,
          "role": BaseTestCase.ROLE_FIRM_ID,
          }, 2, 400),

        ({"username": 'user_name2',
          "first_name": BaseTestCase.USER_NAME * 100,
          "last_name": BaseTestCase.USER_LAST_NAME,
          "email": 'user2@admin.com',
          "password": BaseTestCase.USER_DEFAULT_PASSWORD,
          "role": BaseTestCase.ROLE_FIRM_ID,
          }, 2, 400),

        ({"username": 'user_name2',
          "first_name": BaseTestCase.USER_NAME,
          "last_name": BaseTestCase.USER_LAST_NAME,
          "email": '12354684',
          "password": BaseTestCase.USER_DEFAULT_PASSWORD,
          "role": BaseTestCase.ROLE_FIRM_ID,
          }, 2, 400),

        ({"username": 'user_name2',
          "first_name": BaseTestCase.USER_NAME,
          "last_name": BaseTestCase.USER_LAST_NAME,
          "email": 'user2@admin.com',
          "password": BaseTestCase.USER_DEFAULT_PASSWORD,
          "role": BaseTestCase.ROLE_ID_NOT_EXIST,
          }, 2, 400),

        ({"username": 'user_name2',
          "first_name": BaseTestCase.USER_NAME,
          "last_name": BaseTestCase.USER_LAST_NAME,
          "email": 'user2@admin.com',
          "password": 'Taras' * 10000,
          "role": BaseTestCase.ROLE_FIRM_ID,
          }, 2, 400),
    )

    @data_provider(createuser)
    def test_create_user(self, data, items_count, response_code):
        response = self.client.post(self.url, data, format='json')
        if self.assertEqual(response_code, response.status_code):
            self.assertEqual(len(response.json()), items_count)
