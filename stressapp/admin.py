from django.contrib import admin
from stressapp.models import Recommendation

# Register your models here.

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('stress_level', 'recommend')

admin.site.register(Recommendation, RecommendationAdmin)
