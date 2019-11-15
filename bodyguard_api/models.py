from django.core.management import call_command
from django.db import models
from django.contrib.auth.models import User

User._meta.get_field("email")._unique = True


class Role(models.Model):
    CUSTOMER = 1
    FIRM = 2

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    class Meta:
        db_table = "user_profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="profile", null=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class VariantOptionGuard(models.Model):
    class Meta:
        db_table = "variant"

    name = models.CharField(max_length=50)
    option = models.ForeignKey("OptionGuard", on_delete=models.CASCADE, related_name='variants', null=True)

    def __str__(self):
        return "{}|{}".format(self.option.name, self.name)


class OptionGuard(models.Model):
    class Meta:
        db_table = "option"

    name = models.CharField(max_length=50)

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

    # TYPE_JOB_MAPPING = (
    #     (SOS_TYPE, "SOS"),
    #     (REGULAR_JOB, "Regular order"),
    # )

    type_job = models.IntegerField(choices=TYPE_JOB_CHOICES, default=REGULAR_JOB)
    title = models.CharField(max_length=50, null=True)
    number_guard = models.IntegerField(null=True, blank=True)
    variant = models.ManyToManyField(VariantOptionGuard, related_name='jobs', null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    start_time_guard = models.DateTimeField(null=True)
    end_time_guard = models.DateTimeField(null=True)
    type = models.IntegerField(choices=TYPE_WORK_CHOICES, null=True, default=ONE_TYPE)
    coordinate = models.CharField(max_length=250, null=True)
    comment = models.TextField(null=True, blank=True)
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

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "comment": self.comment,
        }


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
    price = models.FloatField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.job.title)
