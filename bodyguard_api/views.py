from rest_framework import viewsets, mixins
from bodyguard_api.models import *
from bodyguard_api.serializers import UserSerializer, JobSerializer, GuardFirmSerializer, FirmFeedbackSerializer, OrderSerializer
from rest_framework.viewsets import GenericViewSet
from bodyguard_api.permissions import HasPermissionForUser, HasPermissionForJob, \
    HasPermissionForGuardFirm, HasPermissionForOrder, HasPermissionForFirmFeedback


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
