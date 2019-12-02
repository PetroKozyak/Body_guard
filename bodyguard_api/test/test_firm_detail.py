from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


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
