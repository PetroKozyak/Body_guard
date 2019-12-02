from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


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
