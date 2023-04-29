from django.db import models


# Create your models here.
class GPT(models.Model):
    model_name = models.CharField(max_length=30)
    model_description = models.TextField(default="No description")

    class Meta:
        verbose_name = "GPT Model"

    def __str__(self):
        return self.model_name


class Audio(models.Model):
    model_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=30, default="Male")
    short_name = models.CharField(max_length=100, default="Null")
    model_description = models.TextField(default="No description")

    class Meta:
        verbose_name = "Audio Model"

    def __str__(self):
        return self.model_name


class Currency(models.Model):
    symbol = models.CharField(default="¥", max_length=10)
    currency_description = models.TextField(default="日本")

    def __str__(self) -> str:
        return f"{self.symbol} - {self.currency_description}"


class Plan(models.Model):
    plan_name = models.CharField(max_length=30)
    plan_price = models.FloatField()
    unit = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
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


class QaCategory(models.Model):
    first_category = models.CharField(max_length=100, blank=True)
    second_category = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.first_category} - {self.second_category}"

    class Meta:
        verbose_name = "Question Category"


class QA(models.Model):
    category_id = models.ForeignKey(QaCategory, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    audio_path = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.category_id} - {self.question}"

    class Meta:
        verbose_name = "Questions and Answer"
