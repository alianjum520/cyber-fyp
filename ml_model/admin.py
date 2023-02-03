from django.contrib import admin
from .models import (ClassifyCyberBullying, CyberBullyingOrNot, Slang, EthnicityAndRaceGlossary,
                     AgeGlossary, GenderGlossary, ReleigionGlossary, Negation)

# Register your models here.
class CyberBullyingOrNotAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'text_type']
    search_fields = ['text_type']
    list_filter=['text_type']


class ClassifyCyberBullyingAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'text_type']
    search_fields = ['text_type']
    list_filter=['text_type']


class SlangAdmin(admin.ModelAdmin):
    list_display = ['id', 'slang', 'word']


class EthnicityAndRaceGlossaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']


class AgeGlossaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']


class GenderGlossaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']


class ReleigionGlossaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']


class NegationAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']


admin.site.register(CyberBullyingOrNot, CyberBullyingOrNotAdmin)
admin.site.register(ClassifyCyberBullying, ClassifyCyberBullyingAdmin)
admin.site.register(Slang, SlangAdmin)
admin.site.register(EthnicityAndRaceGlossary, EthnicityAndRaceGlossaryAdmin)
admin.site.register(AgeGlossary, AgeGlossaryAdmin)
admin.site.register(GenderGlossary, GenderGlossaryAdmin)
admin.site.register(ReleigionGlossary, ReleigionGlossaryAdmin)
admin.site.register(Negation, NegationAdmin)