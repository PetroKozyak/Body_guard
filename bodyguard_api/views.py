from datetime import datetime
import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from bodyguard import settings
from bodyguard_api.helpers.stripe_helper import StripeHelper
from bodyguard_api.models import *
from bodyguard_api.serializers import UserSerializer, JobSerializer, GuardFirmSerializer, FirmFeedbackSerializer, \
    OrderSerializer, PaySerializer
from rest_framework.viewsets import GenericViewSet
from bodyguard_api.permissions import HasPermissionForUser, HasPermissionForJob, \
    HasPermissionForGuardFirm, HasPermissionForOrder, HasPermissionForFirmFeedback

stripe.api_key = settings.STRIPE_SECRET_KEY

SUCCEEDED = "succeeded"


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


class OrderViewSet(StripeHelper, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [HasPermissionForOrder]

    @action(methods=["post"], detail=True)
    def pay(self, request, pk):
        serializer = PaySerializer(data=request.data)
        order_pay = get_object_or_404(Order, pk=pk)
        result = {"success": False, "errors": []}
        if serializer.is_valid():
            result = StripeHelper.create_charge(self, request, order_pay, result, serializer)
        else:
            result["errors"] = serializer.errors
        return JsonResponse(result)
