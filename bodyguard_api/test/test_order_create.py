import random
from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


class OrderCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("orders-list")

    create_order = lambda: (
        (BaseTestCaseAuthUser.USER_ID_3,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(1, 100000), },
         201,),

        (BaseTestCaseAuthUser.USER_ID_3,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(100001, 99999999), },
         400,),

        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(1, 100000), },
         401,),

        (BaseTestCaseAuthUser.USER_ID_3,
         {"job": BaseTestCaseAuthUser.JOB_NOT_EXIST,
          "price": random.randint(1, 100000), },
         400,),

        (BaseTestCaseAuthUser.USER_ID_2,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(1, 100000), },
         403,),)

    @data_provider(create_order)
    def test_create_order(self, firm_owner, order_data, response_code):
        self.before_test(firm_owner)
        response = self.client.post(self.url, order_data, format='json')
        self.assertEqual(response_code, response.status_code)
