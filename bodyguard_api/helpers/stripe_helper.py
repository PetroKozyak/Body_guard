from datetime import datetime
import stripe
from django.http import JsonResponse

from bodyguard import settings

SUCCEEDED = "succeeded"
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeHelper:
    def create_charge(self, request, order, result, serializer):
        stripe_price = order.stripe_price(order.price)
        try:
            response = stripe.Charge.create(
                amount=stripe_price,
                currency="usd",
                source=request.data.get('token'),  # Done with Stripe.js
                description=order.id
            )
            if response.paid and response.status == SUCCEEDED and response.description == str(order.id) \
                    and response.amount == stripe_price:
                order.pay_date = datetime.now()
                order.transaction_id = response.id
                result["success"] = True
        except Exception as e:
            result["errors"].append(e.user_message)
        return result
