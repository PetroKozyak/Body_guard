from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.models import Job
from bodyguard_api.test.base_test_case import BaseTestCase, BaseTestCaseAuthUser

START_TIME = "2002-02-02 10:10"
END_TIME = "2002-02-03 10:10"
COORDINATE = "2026516.265255"
COMMENT = "testcomment"


class UserCreateAPIViewTestCase(BaseTestCase):
    url = reverse("users-list")

    createuser = lambda: ((
                              {"username": 'user_name1',
                               "first_name": 'Ivan',
                               "last_name": 'Taran',
                               "email": 'user1@admin.com',
                               "password": BaseTestCase.USER_DEFAULT_PASSWORD,
                               "role": BaseTestCase.ROLE_CUSTOMER_ID,
                               }, 2, 201), (
                              {"username": 'user_name2',
                               "first_name": 'Taras',
                               "last_name": 'Kobzar',
                               "email": 'user2@admin.com',
                               "password": BaseTestCase.USER_DEFAULT_PASSWORD,
                               "role": BaseTestCase.ROLE_FIRM_ID,
                               }, 2, 201),)

    @data_provider(createuser)
    def test_create_user(self, data, items_count, response_code):
        response = self.client.post(self.url, data, format='json')
        if self.assertEqual(response_code, response.status_code):
            self.assertEqual(len(response.json()), items_count)


class JobCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("jobs-list")

    OPTION_CAR_VARIANT_YES_ID = 1
    OPTION_CAR_VARIANT_NO_ID = 2
    OPTION_GUN_VARIANT_YES_ID = 3
    OPTION_GUN_VARIANT_NO_ID = 4

    createJob = lambda: (
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": 2,
          "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                      JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": START_TIME,
          "end_time_guard": END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": COORDINATE,
          "comment": COMMENT},
         201,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "number_guard": 2,
          "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                      JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": START_TIME,
          "end_time_guard": END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": COORDINATE,
          "comment": COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": 2,
          "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                      JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": START_TIME,
          "end_time_guard": END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": COORDINATE,
          "comment": COMMENT},
         401,),
    )

    @data_provider(createJob)
    def test_create_job(self, user_id, data, response_code):
        self.before_test(user_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response_code, response.status_code)


class JobDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_job_for_update = lambda: ((BaseTestCaseAuthUser.USER_ID_1,
                                      {"type_job": Job.REGULAR_JOB,
                                       "title": "TestTitle",
                                       "number_guard": 2,
                                       "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                                                   JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
                                       "start_time_guard": START_TIME,
                                       "end_time_guard": END_TIME,
                                       "type": Job.ONE_TYPE,
                                       "customer_id": BaseTestCaseAuthUser.USER_ID_1,
                                       "coordinate": COORDINATE,
                                       "comment": COMMENT},
                                      3,
                                      200,),
                                     (BaseTestCaseAuthUser.USER_ID_1,
                                      {"type_job": Job.SOS_TYPE,
                                       "customer_id": BaseTestCaseAuthUser.USER_ID_1,
                                       "coordinate": COORDINATE},
                                      3,
                                      200,
                                      ),)

    @data_provider(create_job_for_update)
    def test_update_job(self, user_id, data, number_guard, response_code):
        self.before_test(user_id)
        variant = data.pop('variant', [])
        job = Job.objects.create(**data)
        job.variant.set(variant)
        job.save()
        url = reverse("jobs-detail", kwargs={"pk": job.id})
        response = self.client.put(url, {"number_guard": number_guard})
        self.assertEqual(response_code, response.status_code)

    job_delete = lambda: ((BaseTestCaseAuthUser.USER_ID_1,
                           {"type_job": Job.REGULAR_JOB,
                            "title": "TestTitle",
                            "number_guard": 2,
                            "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                                        JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
                            "start_time_guard": START_TIME,
                            "end_time_guard": END_TIME,
                            "type": Job.ONE_TYPE,
                            "customer_id": BaseTestCaseAuthUser.USER_ID_1,
                            "coordinate": COORDINATE,
                            "comment": COMMENT},
                           204,),
                          (BaseTestCaseAuthUser.USER_ID_1,
                           {"type_job": Job.SOS_TYPE,
                            "customer_id": BaseTestCaseAuthUser.USER_ID_1,
                            "coordinate": COORDINATE},
                           204,)
                          ,)

    @data_provider(job_delete)
    def test_delete_job(self, user_id, data, response_code):
        self.before_test(user_id)
        variant = data.pop('variant', [])
        job = Job.objects.create(**data)
        job.variant.set(variant)
        job.save()
        response = self.client.delete(reverse("jobs-detail", kwargs={"pk": job.id}))
        self.assertEqual(response_code, response.status_code)


class FirmCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("guard-list")

    FIRM_DATA = {"name": "TestFirm",
                 "comment": COMMENT}

    create_firm = lambda: (
        (BaseTestCaseAuthUser.USER_ID_1,
         FirmCreateAPIViewTestCase.FIRM_DATA,
         403,),
        (BaseTestCaseAuthUser.USER_ID_2,
         FirmCreateAPIViewTestCase.FIRM_DATA,
         403,),
        (BaseTestCaseAuthUser.USER_ID_4,
         FirmCreateAPIViewTestCase.FIRM_DATA,
         201,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         FirmCreateAPIViewTestCase.FIRM_DATA,
         401,),
    )

    @data_provider(create_firm)
    def test_firm_create(self, user_id, data, response_code):
        self.before_test(user_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response_code, response.status_code)


class FirmDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_firm = lambda: ((BaseTestCaseAuthUser.USER_ID_3,
                            BaseTestCaseAuthUser.FIRM_ID_1,
                            "testcomment_update",
                            200,),
                           )

    @data_provider(create_firm)
    def test_update_firm(self, user_id, firm, comment, response_code):
        self.before_test(user_id)
        url = reverse("guard-detail", kwargs={"pk": firm})
        response = self.client.put(url, {"name": comment})
        self.assertEqual(response_code, response.status_code)

    delete_firm = lambda: ((BaseTestCaseAuthUser.USER_ID_3,
                            BaseTestCaseAuthUser.FIRM_ID_1,
                            204,),
                           (BaseTestCaseAuthUser.USER_ID_1,
                            BaseTestCaseAuthUser.FIRM_ID_1,
                            403,),
                           )

    @data_provider(delete_firm)
    def test_delete_firm(self, user_id, firm, response_code):
        self.before_test(user_id)
        response = self.client.delete(reverse("guard-detail", kwargs={"pk": firm}))
        self.assertEqual(response_code, response.status_code)


class FeedCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("feed_back-list")

    create_feedback = lambda: ((
                                   BaseTestCaseAuthUser.USER_ID_1,
                                   BaseTestCaseAuthUser.FIRM_ID_1,
                                   {"feedback": "not bad",
                                    "firm": BaseTestCaseAuthUser.FIRM_ID_1, },
                                   201,
                               ),
    )

    @data_provider(create_feedback)
    def test_feedback_create(self, user_id, firm, data, response_code):
        self.before_test(user_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response_code, response.status_code)


class FeedDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_feedback = lambda: ((
                                   BaseTestCaseAuthUser.USER_ID_1,
                                   BaseTestCaseAuthUser.FEEDBACK_ID,
                                   204,),
    )

    @data_provider(create_feedback)
    def test_delete_feedback(self, feed_owner_id, feedback, response_code):
        self.before_test(feed_owner_id)
        response = self.client.delete(reverse("feed_back-detail", kwargs={"pk": feedback}))
        self.assertEqual(response_code, response.status_code)

    create_feedback = lambda: ((
                                   BaseTestCaseAuthUser.USER_ID_1,
                                   BaseTestCaseAuthUser.FIRM_ID_1,
                                   BaseTestCaseAuthUser.FEEDBACK_ID,
                                   "test_update_feedback",
                                   200,),
    )

    @data_provider(create_feedback)
    def test_update_feedback(self, feed_owner_id, firm, feedback, comment, response_code):
        self.before_test(feed_owner_id)
        url = reverse("feed_back-detail", kwargs={"pk": feedback})
        response = self.client.put(url, {"feedback": comment, "firm": firm})
        self.assertEqual(response_code, response.status_code)


class OrderCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("orders-list")

    create_order = lambda: ((BaseTestCaseAuthUser.USER_ID_3,
                             {"job": BaseTestCaseAuthUser.JOB_ID_1,
                              "firm_id": BaseTestCaseAuthUser.FIRM_ID_1,
                              "price": 7777, },
                             201,
                             ),)

    @data_provider(create_order)
    def test_create_order(self, firm_owner, order_data, response_code):
        self.before_test(firm_owner)
        response = self.client.post(self.url, order_data, format='json')
        self.assertEqual(response_code, response.status_code)


class OrderDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_order = lambda: ((BaseTestCaseAuthUser.USER_ID_3,
                             BaseTestCaseAuthUser.USER_ID_1,
                             BaseTestCaseAuthUser.ORDER_ID_1,
                             {"job": BaseTestCaseAuthUser.JOB_ID_1,
                              "firm": BaseTestCaseAuthUser.FIRM_ID_1,
                              "price": 88888},
                             200,
                             ),)

    @data_provider(create_order)
    def test_update_order(self, firm_owner, job_owner, order, data, response_code):

        self.before_test(firm_owner)
        url = reverse("orders-detail", kwargs={"pk": order})
        response = self.client.put(url, data)
        if self.assertEqual(response_code, response.status_code):
            self.before_test(job_owner)
            response = self.client.put(url, {"approved": True})
            self.assertEqual(response_code, response.status_code)

    create_order = lambda: ((BaseTestCaseAuthUser.USER_ID_3,
                             BaseTestCaseAuthUser.USER_ID_1,
                             BaseTestCaseAuthUser.ORDER_ID_1,
                             204,
                             403,
                             ),)

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


class PayAPIViewTestCase(BaseTestCaseAuthUser):
    create_stripe = lambda: (
        ("tok_chargeDeclinedExpiredCard",
         ['Your card has expired.'],),
        ("tok_chargeDeclinedProcessingError",
         ['An error occurred while processing your card. Try again in a little bit.'],),
        ("tok_cvcCheckFail",
         ["Your card's security code is incorrect."],),
        ("tok_chargeCustomerFail",
         ['Your card was declined.'],),
        ("tok_riskLevelHighest",
         ['Your card was declined.'],),
        ("tok_chargeDeclined",
         ['Your card was declined.'],),
        ("tok_chargeDeclinedInsufficientFunds",
         ['Your card has insufficient funds.'],),
        ("tok_chargeDeclinedFraudulent",
         ['Your card was declined.'],),
        ("tok_chargeDeclinedIncorrectCvc",
         ["Your card's security code is incorrect."],),)

    @data_provider(create_stripe)
    def test_create_stripe(self, token, errors):
        self.before_test(BaseTestCaseAuthUser.USER_ID_1)
        url = reverse("orders-detail", kwargs={"pk": BaseTestCaseAuthUser.ORDER_ID_1})
        self.client.put(url, {"approved": True})
        url = reverse("orders-pay", kwargs={"pk": BaseTestCaseAuthUser.ORDER_ID_1})
        response = self.client.post(url, {"token": token}, format='json')
        if not response.json().get("success"):
            self.assertEqual(errors, response.json().get("errors"))
