from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.models import Job
from bodyguard_api.test.base_test_case import BaseTestCase, BaseTestCaseAuthUser


class UserCreateAPIViewTestCase(BaseTestCase):
    url = reverse("users-list")

    createuser = lambda: (
        ('user_name1', 'Ivan', 'Taran', 'user1@admin.com', 'adminadmin', BaseTestCase.ROLE_CUSTOMER_ID, 2, 201),
        ('user_name2', 'Taras', 'Baran', 'user2@admin.com', 'adminadmin', BaseTestCase.ROLE_FIRM_ID, 2, 201),
    )

    @data_provider(createuser)
    def test_create_user(self, username, first_name, last_name, email, password, role, items_count, response_code):
        data = {"username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "role": role,
                }
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
          "start_time_guard": "2002-02-02 10:10",
          "end_time_guard": "2002-02-03 10:10",
          "type": Job.ONE_TYPE,
          "coordinate": "2026516.265255",
          "comment": "testcomment"},
         201,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "number_guard": 2,
          "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                      JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": "2002-02-02 10:10",
          "end_time_guard": "2002-02-03 10:10",
          "type": Job.ONE_TYPE,
          "coordinate": "2026516.265255",
          "comment": "testcomment"},
         400,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": 2,
          "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                      JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": "2002-02-02 10:10",
          "end_time_guard": "2002-02-03 10:10",
          "type": Job.ONE_TYPE,
          "coordinate": "2026516.265255",
          "comment": "testcomment"},
         401,),
    )

    @data_provider(createJob)
    def test_create_job(self, user_id, data, response_code):
        self.before_test(user_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response_code, response.status_code)


class JobDetailAPIViewTestCase(BaseTestCaseAuthUser):
    createJob_for_update = lambda: ((BaseTestCaseAuthUser.USER_ID_1,
                                     {"type_job": Job.REGULAR_JOB,
                                      "title": "TestTitle",
                                      "number_guard": 2,
                                      "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                                                  JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
                                      "start_time_guard": "2022-02-02 10:10",
                                      "end_time_guard": "2022-02-03 10:10",
                                      "type": Job.ONE_TYPE,
                                      "customer_id": BaseTestCaseAuthUser.USER_ID_1,
                                      "coordinate": "2026516.265255",
                                      "comment": "testcomment"},
                                     200,),
                                    (BaseTestCaseAuthUser.USER_ID_1,
                                     {"type_job": Job.SOS_TYPE,
                                      "customer_id": BaseTestCaseAuthUser.USER_ID_1,
                                      "coordinate": "2026516.265255"},
                                     200,
                                     ),)

    @data_provider(createJob_for_update)
    def test_update_job(self, user_id, data, response_code):
        self.before_test(user_id)
        variant = data.pop('variant', [])
        job = Job.objects.create(**data)
        job.variant.set(variant)
        job.save()
        url = reverse("jobs-detail", kwargs={"pk": job.id})
        response = self.client.put(url, {"number_guard": 3})
        self.assertEqual(response_code, response.status_code)

    job_delete = lambda: ((BaseTestCaseAuthUser.USER_ID_1,
                           {"type_job": Job.REGULAR_JOB,
                            "title": "TestTitle",
                            "number_guard": 2,
                            "variant": [JobCreateAPIViewTestCase.OPTION_CAR_VARIANT_YES_ID,
                                        JobCreateAPIViewTestCase.OPTION_GUN_VARIANT_NO_ID],
                            "start_time_guard": "2022-02-02 10:10",
                            "end_time_guard": "2022-02-03 10:10",
                            "type": Job.ONE_TYPE,
                            "customer_id": BaseTestCaseAuthUser.USER_ID_1,
                            "coordinate": "2026516.265255",
                            "comment": "testcomment"},
                           204,),
                          (BaseTestCaseAuthUser.USER_ID_1,
                           {"type_job": Job.SOS_TYPE,
                            "customer_id": BaseTestCaseAuthUser.USER_ID_1,
                            "coordinate": "2026516.265255"},
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
                 "comment": "testcomment"}

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
                            200,),
                           )

    @data_provider(create_firm)
    def test_update_firm(self, user_id, firm, response_code):
        self.before_test(user_id)
        url = reverse("guard-detail", kwargs={"pk": firm})
        response = self.client.put(url, {"name": "testcomment_update"})
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
                                   201,
                               ),
    )

    @data_provider(create_feedback)
    def test_feedback_create(self, user_id, firm, response_code):
        data = {
            "feedback": "not bad",
            "firm": firm,
        }
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
                                   200,),
    )

    @data_provider(create_feedback)
    def test_update_feedback(self, feed_owner_id, firm, feedback, response_code):
        self.before_test(feed_owner_id)
        url = reverse("feed_back-detail", kwargs={"pk": feedback})
        response = self.client.put(url, {"feedback": "test_update_feedback", "firm": firm})
        self.assertEqual(response_code, response.status_code)


class OrderCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("orders-list")

    create_order = lambda: ((BaseTestCaseAuthUser.USER_ID_3,
                             BaseTestCaseAuthUser.FIRM_ID_1,
                             BaseTestCaseAuthUser.JOB_ID_1,
                             201,
                             ),)

    @data_provider(create_order)
    def test_create_order(self, firm_owner, firm, job, response_code):
        self.before_test(firm_owner)
        order_data = {
            "job": job,
            "firm_id": firm,
            "price": 10500,
        }
        response = self.client.post(self.url, order_data, format='json')
        self.assertEqual(response_code, response.status_code)


class OrderDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_order = lambda: ((BaseTestCaseAuthUser.USER_ID_3,
                             BaseTestCaseAuthUser.USER_ID_1,
                             BaseTestCaseAuthUser.FIRM_ID_1,
                             BaseTestCaseAuthUser.JOB_ID_1,
                             BaseTestCaseAuthUser.ORDER_ID_1,
                             200,
                             ),)

    @data_provider(create_order)
    def test_update_order(self, firm_owner, job_owner, firm, job, order, response_code):

        self.before_test(firm_owner)
        url = reverse("orders-detail", kwargs={"pk": order})
        response = self.client.put(url, {"job": job, "firm": firm, "price": 88888})
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

