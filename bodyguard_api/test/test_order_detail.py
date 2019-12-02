import random
from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


class OrderDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_order = lambda: (
        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_ID_1,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(1, 100000)},
         200, 200,),

        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_ID_1,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(100001, 9999999)},
         400, 200,),

        (BaseTestCaseAuthUser.USER_ID_2,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_ID_1,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(1, 100000)},
         403, 200,),

        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_ID_1,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(1, 100000)},
         401, 200,),

        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.ORDER_ID_1,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(1, 100000)},
         200, 403,),

        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_NOT_EXIST,
         {"job": BaseTestCaseAuthUser.JOB_ID_1,
          "price": random.randint(1, 100000)},
         404, 200,),

        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_ID_1,
         {"job": BaseTestCaseAuthUser.JOB_NOT_EXIST,
          "price": random.randint(1, 100000)},
         400, 200,),

        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_ID_1,
         {"job": BaseTestCaseAuthUser.JOB_ID_2_SOS,
          "price": random.randint(1, 100000)},
         200, 200,),
    )

    @data_provider(create_order)
    def test_update_order(self, firm_owner, job_owner, order, data, response_code_data_order,
                          response_code_order_approved):
        self.before_test(firm_owner)
        url = reverse("orders-detail", kwargs={"pk": order})
        response = self.client.put(url, data)
        if self.assertEqual(response_code_data_order, response.status_code):
            self.before_test(job_owner)
            response = self.client.put(url, {"approved": True})
            self.assertEqual(response_code_order_approved, response.status_code)

    create_order = lambda: (

        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_ID_1,
         204, 403,),

        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_NOT_EXIST,
         404, 403,),

        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.ORDER_ID_1,
         401, 403,),

        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.ORDER_ID_1,
         404, 403,),)

    @data_provider(create_order)
    def test_delete_order(self, firm_owner, job_owner, order, response_code_not_approved,
                          response_code_approved):

        self.before_test(firm_owner)
        response = self.client.delete(reverse("orders-detail", kwargs={"pk": order}))
        if self.assertEqual(response_code_not_approved, response.status_code):
            self.before_test(job_owner)
            url = reverse("orders-detail", kwargs={"pk": order})
            self.client.put(url, {"approved": True})
            self.before_test(firm_owner)
            response = self.client.delete(reverse("orders-detail", kwargs={"pk": order}))
            self.assertEqual(response_code_approved, response.status_code)
