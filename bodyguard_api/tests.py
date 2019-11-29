import random
from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.models import Job
from bodyguard_api.test.base_test_case import BaseTestCase, BaseTestCaseAuthUser


class UserCreateAPIViewTestCase(BaseTestCase):
    url = reverse("users-list")

    createuser = lambda: (({"username": 'user_name1',
                            "first_name": 'Ivan',
                            "last_name": 'Taran',
                            "email": 'user1@admin.com',
                            "password": BaseTestCase.USER_DEFAULT_PASSWORD,
                            "role": BaseTestCase.ROLE_CUSTOMER_ID,
                            }, 2, 201),
                          ({"username": 'user_name2',
                            "first_name": 'Taras',
                            "last_name": 'Kobzar',
                            "email": 'user2@admin.com',
                            "password": BaseTestCase.USER_DEFAULT_PASSWORD,
                            "role": BaseTestCase.ROLE_FIRM_ID,
                            }, 2, 201),
                          ({"username": 'user_name2' * 100,
                            "first_name": 'Taras',
                            "last_name": 'Kobzar',
                            "email": 'user2@admin.com',
                            "password": BaseTestCase.USER_DEFAULT_PASSWORD,
                            "role": BaseTestCase.ROLE_FIRM_ID,
                            }, 2, 400),
                          ({"username": 'user_name2',
                            "first_name": 'Taras' * 100,
                            "last_name": 'Kobzar',
                            "email": 'user2@admin.com',
                            "password": BaseTestCase.USER_DEFAULT_PASSWORD,
                            "role": BaseTestCase.ROLE_FIRM_ID,
                            }, 2, 400),
                          ({"username": 'user_name2',
                            "first_name": 'Taras',
                            "last_name": 'Kobzar',
                            "email": '12354684',
                            "password": BaseTestCase.USER_DEFAULT_PASSWORD,
                            "role": BaseTestCase.ROLE_FIRM_ID,
                            }, 2, 400),
                          ({"username": 'user_name2',
                            "first_name": 'user_name2',
                            "last_name": 'user_name2',
                            "email": 'user2@admin.com',
                            "password": 'user_name2',
                            "role": BaseTestCase.ROLE_FIRM_ID,
                            }, 2, 400),
                          ({"username": 'user_name2',
                            "first_name": 'Taras',
                            "last_name": 'Kobzar',
                            "email": 'user2@admin.com',
                            "password": BaseTestCase.USER_DEFAULT_PASSWORD,
                            "role": BaseTestCase.ROLE_ID_NOT_EXIST,
                            }, 2, 400),
                          ({"username": 'user_name2',
                            "first_name": 'Taras',
                            "last_name": 'Kobzar',
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


class JobCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("jobs-list")

    createJob = lambda: (
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT},
         201,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT},
         401,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle" * 100,
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": random.randint(11, 99999999),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.BAD_START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.BAD_END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": 0,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE * 500,
          "comment": BaseTestCaseAuthUser.COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"type_job": Job.REGULAR_JOB,
          "title": "TestTitle",
          "number_guard": random.randint(1, 10),
          "variant": [BaseTestCaseAuthUser.OPTION_CAR_VARIANT_YES_ID,
                      BaseTestCaseAuthUser.OPTION_GUN_VARIANT_NO_ID],
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": Job.ONE_TYPE,
          "coordinate": BaseTestCaseAuthUser.COORDINATE,
          "comment": BaseTestCaseAuthUser.COMMENT * 40000},
         400,),
    )

    @data_provider(createJob)
    def test_create_job(self, user_id, data, response_code):
        self.before_test(user_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response_code, response.status_code)


class JobDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_job_for_update = lambda: (
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         200,),
        (BaseTestCaseAuthUser.USER_ID_2,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         403,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         401,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.BAD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.BAD_START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.BAD_END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.BAD_END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.BAD_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.BAD_JOB_TYPE,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.BAD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.BAD_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,
          "end_time_guard": BaseTestCaseAuthUser.END_TIME,
          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.BAD_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_3_REGULAR,
         {"title": BaseTestCaseAuthUser.UPDATE_TITLE,
          "number_guard": BaseTestCaseAuthUser.GOOD_NUMBER_GUARD,
          "variant": BaseTestCaseAuthUser.GOOD_VARIANTS,
          "start_time_guard": BaseTestCaseAuthUser.START_TIME,

          "type": BaseTestCaseAuthUser.TYPE_JOB_REGULAR,
          "coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_2_SOS,
         {"coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE},
         200,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         BaseTestCaseAuthUser.JOB_ID_2_SOS,
         {"coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE},
         401,),
        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.JOB_ID_2_SOS,
         {"coordinate": BaseTestCaseAuthUser.UPDATE_COORDINATE},
         403,),
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_2_SOS,
         {"coordinate": BaseTestCaseAuthUser.BAD_COORDINATE},
         400,),

    )

    @data_provider(create_job_for_update)
    def test_update_job(self, user_id, job, data,
                        response_code):
        self.before_test(user_id)
        url = reverse("jobs-detail", kwargs={"pk": job})
        response = self.client.put(url, data)
        print(response.content)
        self.assertEqual(response_code, response.status_code)

    job_delete = lambda: (
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.JOB_ID_1,
         204,),
        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.JOB_ID_1,
         403,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         BaseTestCaseAuthUser.JOB_ID_1,
         401,),
        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.JOB_NOT_EXIST,
         403,),
    )

    @data_provider(job_delete)
    def test_delete_job(self, user_id, data, response_code):
        self.before_test(user_id)
        response = self.client.delete(reverse("jobs-detail", kwargs={"pk": data}))
        self.assertEqual(response_code, response.status_code)


class FirmCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("guard-list")

    FIRM_DATA = {"name": "TestFirm",
                 "comment": BaseTestCaseAuthUser.COMMENT}

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
         401,)
    )

    @data_provider(create_firm)
    def test_firm_create(self, user_id, data, response_code):
        self.before_test(user_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response_code, response.status_code)


class FirmDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_firm = lambda: (
        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.FIRM_ID_1,
         {"name": BaseTestCaseAuthUser.NEW_NAME_FIRM,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         200,),
        (BaseTestCaseAuthUser.USER_ID_2,
         BaseTestCaseAuthUser.FIRM_ID_1,
         {"name": BaseTestCaseAuthUser.NEW_NAME_FIRM,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         403,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         BaseTestCaseAuthUser.FIRM_ID_1,
         {"name": BaseTestCaseAuthUser.NEW_NAME_FIRM,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         401,),
        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.FIRM_ID_1,
         {"name": BaseTestCaseAuthUser.NEW_BAD_NAME_FIRM,
          "comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.FIRM_ID_1,
         {"comment": BaseTestCaseAuthUser.UPDATE_COMMENT},
         400,),
        (BaseTestCaseAuthUser.USER_ID_3,
         BaseTestCaseAuthUser.FIRM_ID_1,
         {"name": BaseTestCaseAuthUser.NEW_NAME_FIRM},
         200,),
    )

    @data_provider(create_firm)
    def test_update_firm(self, user_id, firm, data, response_code):
        self.before_test(user_id)
        url = reverse("guard-detail", kwargs={"pk": firm})
        response = self.client.put(url, data)
        self.assertEqual(response_code, response.status_code)

    delete_firm = lambda: ((BaseTestCaseAuthUser.USER_ID_3,
                            BaseTestCaseAuthUser.FIRM_ID_1,
                            204,),
                           (BaseTestCaseAuthUser.USER_ID_1,
                            BaseTestCaseAuthUser.FIRM_ID_1,
                            403,),
                           (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
                            BaseTestCaseAuthUser.FIRM_ID_1,
                            401,),
                           (BaseTestCaseAuthUser.USER_ID_3,
                            BaseTestCaseAuthUser.FIRM_NOT_EXIST,
                            404,),
                           )

    @data_provider(delete_firm)
    def test_delete_firm(self, user_id, firm, response_code):
        self.before_test(user_id)
        response = self.client.delete(reverse("guard-detail", kwargs={"pk": firm}))
        self.assertEqual(response_code, response.status_code)


class FeedCreateAPIViewTestCase(BaseTestCaseAuthUser):
    url = reverse("feed_back-list")

    create_feedback = lambda: (
        (BaseTestCaseAuthUser.USER_ID_1,
         {"feedback": "not bad",
          "firm": BaseTestCaseAuthUser.FIRM_ID_1, },
         201,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         {"feedback": "not bad",
          "firm": BaseTestCaseAuthUser.FIRM_ID_1, },
         401,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"feedback": "not bad",
          "firm": BaseTestCaseAuthUser.FIRM_NOT_EXIST, },
         400,),
    )

    @data_provider(create_feedback)
    def test_feedback_create(self, user_id, data, response_code):
        self.before_test(user_id)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response_code, response.status_code)


class FeedDetailAPIViewTestCase(BaseTestCaseAuthUser):
    create_feedback = lambda: (
        (BaseTestCaseAuthUser.USER_ID_1,
         BaseTestCaseAuthUser.FEEDBACK_ID,
         204,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         BaseTestCaseAuthUser.FEEDBACK_ID,
         401,),
        (BaseTestCaseAuthUser.USER_ID_2,
         BaseTestCaseAuthUser.FEEDBACK_ID,
         404,),
    )

    @data_provider(create_feedback)
    def test_delete_feedback(self, feed_owner_id, feedback, response_code):
        self.before_test(feed_owner_id)
        response = self.client.delete(reverse("feed_back-detail", kwargs={"pk": feedback}))
        self.assertEqual(response_code, response.status_code)

    update_feedback = lambda: (
        (BaseTestCaseAuthUser.USER_ID_1,
         {"firm": BaseTestCaseAuthUser.FIRM_ID_1,
          "feedback": "test_update_feedback"},
         BaseTestCaseAuthUser.FEEDBACK_ID,
         200,),
        (BaseTestCaseAuthUser.USER_ID_5_NOT_EXIST,
         {"firm": BaseTestCaseAuthUser.FIRM_ID_1,
          "feedback": "test_update_feedback"},
         BaseTestCaseAuthUser.FEEDBACK_ID,
         401,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"firm": BaseTestCaseAuthUser.FIRM_NOT_EXIST,
          "feedback": "test_update_feedback"},
         BaseTestCaseAuthUser.FEEDBACK_ID,
         400,),
        (BaseTestCaseAuthUser.USER_ID_1,
         {"firm": BaseTestCaseAuthUser.FIRM_ID_1,
          "feedback": "test_update_feedback"},
         BaseTestCaseAuthUser.FEEDBACK_NOT_EXIST,
         404,),
    )

    @data_provider(update_feedback)
    def test_update_feedback(self, feed_owner_id, data, feedback, response_code):
        self.before_test(feed_owner_id)
        url = reverse("feed_back-detail", kwargs={"pk": feedback})
        response = self.client.put(url, data)
        self.assertEqual(response_code, response.status_code)


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
