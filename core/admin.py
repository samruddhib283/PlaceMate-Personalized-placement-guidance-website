from django.contrib import admin
from .models import Opportunity
from .models import SuccessStory

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'last_date')
    search_fields = ('title', 'category')
    list_filter = ('category', 'last_date')


admin.site.register(SuccessStory)
