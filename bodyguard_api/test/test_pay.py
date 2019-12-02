from unittest_data_provider import data_provider
from django.urls import reverse
from bodyguard_api.test.base_test_case import BaseTestCaseAuthUser


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
