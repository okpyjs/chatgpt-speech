from django.db import models


# Create your models here.
class GPT(models.Model):
    model_name = models.CharField(max_length=30)
    model_description = models.TextField()

    class Meta:
        verbose_name = "GPT Model"

    def __str__(self):
        return self.model_name


class Audio(models.Model):
    model_name = models.CharField(max_length=30)
    model_description = models.TextField()

    class Meta:
        verbose_name = "Audio Model"

    def __str__(self):
        return self.model_name


class PayUnit(models.Model):
    unit_name = models.CharField(default="¥", max_length=10)
    unit_description = models.TextField(default="日本")

    def __str__(self) -> str:
        return self.unit_description


class Plan(models.Model):
    plan_name = models.CharField(max_length=30)
    plan_price = models.FloatField()
    unit = models.ForeignKey(PayUnit, on_delete=models.DO_NOTHING)
    request_no_per_day = models.IntegerField()
    plan_description = models.TextField(default="No description")

    def __str__(self) -> str:
        return self.plan_name


class PlanSettingGpt(models.Model):
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    model_id = models.ForeignKey(GPT, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.plan_id} -> GPT Model({self.model_id})"


class PlanSettingAudio(models.Model):
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    model_id = models.ForeignKey(Audio, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.plan_id} -> Audio Model({self.model_id})"
