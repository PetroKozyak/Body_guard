from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


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
