import random
from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.models import Job
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


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
