from django.contrib import admin
from gpt_audio_model.models import GPT, Audio

# Register your models here.


class AudioAdmin(admin.ModelAdmin):
    pass


class GptAdmin(admin.ModelAdmin):
    pass


admin.site.register(GPT, GptAdmin)
admin.site.register(Audio, AudioAdmin)
