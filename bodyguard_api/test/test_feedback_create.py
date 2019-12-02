from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


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
