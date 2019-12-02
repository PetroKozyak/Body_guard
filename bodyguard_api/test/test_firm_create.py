from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


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
