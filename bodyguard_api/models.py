from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

User._meta.get_field("email")._unique = True


class Role(models.Model):
    CUSTOMER = 1
    FIRM = 2

    TYPE_ROLE = ((CUSTOMER, "Customer"),
                 (FIRM, "Firm"),)

    name = models.IntegerField(choices=TYPE_ROLE, default=CUSTOMER)

    def __str__(self):
        return '{}'.format(self.get_name_display())


class UserProfile(models.Model):
    class Meta:
        db_table = "user_profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="profile", default=Role.CUSTOMER)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class VariantOptionGuard(models.Model):
    name = models.CharField(max_length=50)
    option = models.ForeignKey("OptionGuard", on_delete=models.CASCADE, related_name='variants')

    class Meta:
        db_table = "variant"
        unique_together = ('name', 'option',)

    def __str__(self):
        return "{}|{}".format(self.option.name, self.name)


class OptionGuard(models.Model):
    class Meta:
        db_table = "option"

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Job(models.Model):
    class Meta:
        db_table = "jobs"

    ONE_TYPE = 1
    REGULAR_TYPE = 2

    TYPE_WORK_CHOICES = ((ONE_TYPE, "One time"),
                         (REGULAR_TYPE, "Regular"),)

    SOS_TYPE = 1
    REGULAR_JOB = 2

    TYPE_JOB_CHOICES = ((SOS_TYPE, "SOS"),
                        (REGULAR_JOB, "Regular order"),)

    type_job = models.IntegerField(choices=TYPE_JOB_CHOICES, default=REGULAR_JOB)
    title = models.CharField(max_length=50, null=True)
    number_guard = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    variant = models.ManyToManyField(VariantOptionGuard, related_name='jobs', null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    start_time_guard = models.DateTimeField(null=True)
    end_time_guard = models.DateTimeField(null=True)
    type = models.IntegerField(choices=TYPE_WORK_CHOICES, null=True, default=ONE_TYPE)
    coordinate = models.CharField(max_length=100, null=True)
    comment = models.TextField(max_length=500, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.type_job == self.SOS_TYPE:
            return 'SOS'
        else:
            return "{}".format(self.title)


class GuardFirm(models.Model):
    class Meta:
        db_table = "guard_firm"

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="guard_firm")
    name = models.CharField(max_length=250)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class FirmFeedback(models.Model):
    class Meta:
        db_table = "feed_backs"

    feedback = models.TextField(null=True, blank=True)
    firm = models.ForeignKey("GuardFirm", on_delete=models.CASCADE, related_name='feed_backs')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feed_backs")

    def __str__(self):
        return "{}".format(self.feedback)


class Order(models.Model):
    class Meta:
        db_table = "orders"

    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='orders')
    firm = models.ForeignKey(GuardFirm, on_delete=models.CASCADE, related_name='orders')
    price = models.FloatField(blank=True, validators=[MinValueValidator(1), MaxValueValidator(100000)])
    approved = models.BooleanField(default=False)
    pay_date = models.DateTimeField(null=True)
    transaction_id = models.IntegerField(null=True)

    def stripe_price(self, value):
        stripe_price = value * 100
        return int(stripe_price)

    def __str__(self):
        return "{}".format(self.job.title)
