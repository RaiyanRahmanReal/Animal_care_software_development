from django.contrib import admin
from .models import Petadd
from .models import DaycareRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import mark_safe
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from .models import DaycareRequest

class PetAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'breed',
        'owner',
        'is_approved',
        'is_for_adoption',
        'sold',
        'buyer',
        'adopter'
    ]
    list_filter = ['is_approved', 'owner', 'breed', 'sold', 'is_for_adoption']
    actions = ['approve_pets']

    def approve_pets(self, request, queryset):
        pets_to_approve = queryset.filter(is_approved=False)
        count = pets_to_approve.update(is_approved=True)

        if count:
            self.message_user(request, f'{count} pet(s) approved successfully.')
        else:
            self.message_user(request, 'No pets were selected for approval.')

    approve_pets.short_description = "Approve selected pets"


admin.site.register(Petadd, PetAdmin)





@admin.register(DaycareRequest)
class DaycareRequestAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'user', 'start_date', 'end_date', 'status', 'pet_photo_thumbnail', 'accepted_by')
    list_filter = ('approved', 'rejected', 'accepted_by')
    search_fields = ('pet_name', 'user__username', 'breed', 'accepted_by__username')
    actions = ['approve_requests', 'reject_requests']
    readonly_fields = ('accepted_by',)  # Prevent direct editing of 'accepted_by'

    def pet_photo_thumbnail(self, obj):
        if obj.pet_photo:
            return mark_safe(f'<img src="{obj.pet_photo.url}" width="50" />')
        return 'No Image'
    pet_photo_thumbnail.short_description = 'Pet Photo'

    def approve_requests(self, request, queryset):
        queryset = queryset.filter(approved=False, rejected=False)
        if not queryset.exists():
            self.message_user(request, "No pending requests to approve.")
            return
        queryset.update(approved=True, rejected=False)
        self.message_user(request, "Selected requests have been approved.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    approve_requests.short_description = "Approve selected requests"

    def reject_requests(self, request, queryset):
        queryset = queryset.filter(approved=False, rejected=False)
        if not queryset.exists():
            self.message_user(request, "No pending requests to reject.")
            return
        queryset.update(approved=False, rejected=True)
        self.message_user(request, "Selected requests have been rejected.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    reject_requests.short_description = "Reject selected requests"

    def status(self, obj):
        if obj.approved:
            return "Approved"
        elif obj.rejected:
            return "Rejected"
        else:
            return "Pending"
    status.short_description = 'Status'




