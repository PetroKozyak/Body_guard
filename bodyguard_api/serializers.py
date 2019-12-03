import stripe
from django.conf import settings
from rest_framework import serializers
from bodyguard_api.models import *
from bodyguard_api.permissions import CREATE_METHOD, UPDATE_METHOD, PATCH_METHOD



class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role.TYPE_ROLE, default=Role.CUSTOMER)
    password_confirm = serializers.CharField(required=False)

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        if instance.profile:
            data['role'] = instance.profile.role.get_name_display()
        return data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_confirm", None)
        role = validated_data.pop('role')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        role = Role.objects.get(name=role)
        user.profile.role = role
        user.profile.save()
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirm",
            "role",
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
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

        if action in [CREATE_METHOD, UPDATE_METHOD]:
            if data.get('type_job') == Job.REGULAR_JOB or self.instance.type_job == Job.REGULAR_JOB:
                errors = {key: 'This field is required' for key in self.fields.keys()
                          if not data.get(key) and key not in ['id', 'comment', 'customer', 'date_created', 'type_job']}
                if errors:
                    raise serializers.ValidationError(errors)
                if data.get('start_time_guard') > data.get('end_time_guard'):
                    raise serializers.ValidationError("Finish must occur after start")

        return data

    def get_extra_kwargs(self):
        extra_kwargs = super(JobSerializer, self).get_extra_kwargs()
        action = self.context['view'].action

        if action is UPDATE_METHOD and self.instance.customer == self.context['request'].user:
            kwargs = extra_kwargs.get('type_job', {})
            kwargs['read_only'] = True
            extra_kwargs['type_job'] = kwargs

        return extra_kwargs

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('id', 'customer', 'date_created',)

        extra_kwargs = {
            'type_job': {'read_only': False}
        }


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

        if action in [UPDATE_METHOD, PATCH_METHOD] and self.instance.job.customer == self.context['request'].user:
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
        data['job'] = JobSerializer(instance.job, context={'view': self.context['view'],
                                                           'request': self.context['request']}).data

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
