import stripe
from django.conf import settings
from rest_framework import serializers
from bodyguard_api.models import *
from bodyguard_api.permissions import CREATE_METHOD

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=tuple(Role.objects.values_list('id', 'name')), default=Role.CUSTOMER)

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data['role'] = instance.profile.role.name
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        role = Role.objects.get(pk=role)
        instance = User.objects.create(**validated_data)
        instance.profile.role = role
        instance.profile.save()
        return instance

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class VariantOptionGuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantOptionGuard
        fields = '__all__'

    def to_representation(self, instance):
        data = super(VariantOptionGuardSerializer, self).to_representation(instance)
        data['option'] = instance.option.name
        return data


class JobSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(JobSerializer, self).to_representation(instance)
        data['variant'] = VariantOptionGuardSerializer(instance.variant, many=True).data
        data['type'] = instance.get_type_display() if instance.type else None
        data['type_job'] = instance.get_type_job_display() if instance.type_job else None
        return data

    def validate_variant(self, value):
        options_ids = []
        for val in value:
            if val.option.id in options_ids:
                raise serializers.ValidationError("{} - you'd select two variants from one option. "
                                                  "Please select one".format(val))
            options_ids.append(val.option.id)
        return value

    def validate(self, data):
        action = self.context['view'].action
        if action == CREATE_METHOD:
            if data.get('type_job') == Job.REGULAR_JOB:
                errors = {key: 'This field is required' for key in self.fields.keys()
                          if not data.get(key) and key not in ['id', 'comment', 'type', 'customer', 'date_created']}
                if errors:
                    raise serializers.ValidationError(errors)
                if data.get('start_time_guard') > data.get('end_time_guard'):
                    raise serializers.ValidationError("Finish must occur after start")
        return data

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('id', 'customer', 'date_created',)


class OptionGuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionGuard
        fields = '__all__'


class GuardFirmSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    def save(self, **kwargs):
        kwargs["owner"] = self.fields["owner"].get_default()
        return super().save(**kwargs)

    class Meta:
        model = GuardFirm
        fields = '__all__'


class FirmFeedbackSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    def save(self, **kwargs):
        kwargs["customer"] = self.fields["customer"].get_default()
        return super().save(**kwargs)

    def to_representation(self, instance):
        data = super(FirmFeedbackSerializer, self).to_representation(instance)
        data['firm'] = GuardFirmSerializer(instance.firm).data
        return data

    class Meta:
        model = FirmFeedback
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'job', 'firm', 'price', 'approved')
        read_only_fields = ('firm',)

        extra_kwargs = {
            'approved': {'read_only': True},
            'job': {'read_only': False},
            'price': {'read_only': False, 'required': True},
            'pay_date': {'read_only': True},
            'transaction_id': {'read_only': True},
        }

    def save(self, **kwargs):
        user = self.context["request"].user
        if self.context["request"].method == "POST":
            kwargs["firm"] = user.guard_firm
        return super().save(**kwargs)

    def create(self, validated_data):
        job = validated_data.get('job')
        if job.type_job == Job.SOS_TYPE:
            validated_data['approved'] = True
        return Order.objects.create(**validated_data)

    def get_extra_kwargs(self):
        extra_kwargs = super(OrderSerializer, self).get_extra_kwargs()
        action = self.context['view'].action

        if action in ['update', 'partial_update'] and self.instance.job.customer == self.context['request'].user:
            kwargs = extra_kwargs.get('approved', {})
            kwargs['read_only'] = False
            extra_kwargs['approved'] = kwargs

            kwargs = extra_kwargs.get('job', {})
            kwargs['read_only'] = True
            extra_kwargs['job'] = kwargs

            kwargs = extra_kwargs.get('price', {})
            kwargs['read_only'] = True
            extra_kwargs['price'] = kwargs

        return extra_kwargs

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        data['firm'] = GuardFirmSerializer(instance.firm).data
        data['job'] = JobSerializer(instance.job).data

        return data


class PaySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, validate_data):
        token = validate_data.get('token')
        try:
            validate_token = stripe.Token.retrieve(token)
            if validate_token.used:
                raise serializers.ValidationError({'token': 'This token is already used.'})
        except Exception as e:
            raise serializers.ValidationError({'token': 'This token is invalid.'})
        return validate_data
