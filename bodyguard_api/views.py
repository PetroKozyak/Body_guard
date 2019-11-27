from datetime import datetime
import stripe
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from bodyguard import settings
from bodyguard_api.models import *
from bodyguard_api.serializers import UserSerializer, JobSerializer, GuardFirmSerializer, FirmFeedbackSerializer, \
    OrderSerializer, PaySerializer
from rest_framework.viewsets import GenericViewSet
from bodyguard_api.permissions import HasPermissionForUser, HasPermissionForJob, \
    HasPermissionForGuardFirm, HasPermissionForOrder, HasPermissionForFirmFeedback

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin, GenericViewSet):
    queryset = User.objects.prefetch_related("profile").select_related(
        "profile"
    )
    serializer_class = UserSerializer
    permission_classes = (HasPermissionForUser,)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [HasPermissionForJob]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class GuardFirmViewSet(viewsets.ModelViewSet):
    queryset = GuardFirm.objects.all()
    serializer_class = GuardFirmSerializer
    permission_classes = [HasPermissionForGuardFirm]


class FirmFeedbackViewSet(viewsets.ModelViewSet):
    queryset = FirmFeedback.objects.all()
    serializer_class = FirmFeedbackSerializer
    permission_classes = [HasPermissionForFirmFeedback]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [HasPermissionForOrder]

    @action(methods=["post"], detail=True)
    def pay(self, request, pk):
        serializer = PaySerializer(data=request.data)
        order = Order.objects.get(pk=pk)
        result = {"success": False, "errors": []}
        if serializer.is_valid():
            try:
                response = stripe.Charge.create(
                    amount=int(order.price) * 100,
                    currency="usd",
                    source=request.data["token"],  # Done with Stripe.js
                    description=order.id
                )
                if response.paid and response.status == "succeeded" and response.description == str(order.id) \
                        and response.amount == int(order.price) * 100:
                    order.pay_date = datetime.now()
                    order.transaction_id = response.id
                    result["success"] = True
            except Exception as e:
                result["errors"].append(e.user_message)
        else:
            result["errors"] = serializer.errors
        return JsonResponse(result)
