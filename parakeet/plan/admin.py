from django.contrib import admin
from plan.models import (
    GPT,
    QA,
    Audio,
    Currency,
    Plan,
    PlanSettingAudio,
    PlanSettingGpt,
    QaCategory,
)


# Register your models here.
class AudioAdmin(admin.ModelAdmin):
    pass


class GPTAdmin(admin.ModelAdmin):
    pass


class PlanAdmin(admin.ModelAdmin):
    pass


class PlanSettingAudioAdmin(admin.ModelAdmin):
    pass


class PlanSettingGptAdmin(admin.ModelAdmin):
    pass


class PayUnitAdmin(admin.ModelAdmin):
    pass


class QAAdmin(admin.ModelAdmin):
    pass


class QaCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Audio, AudioAdmin)
admin.site.register(GPT, GPTAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(PlanSettingAudio, PlanSettingAudioAdmin)
admin.site.register(PlanSettingGpt, PlanSettingGptAdmin)
admin.site.register(Currency, PayUnitAdmin)
admin.site.register(QA, QAAdmin)
admin.site.register(QaCategory, QaCategoryAdmin)
