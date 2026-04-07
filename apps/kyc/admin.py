from django.contrib import admin
from .models import KYC
from django.utils.html import format_html


@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "submitted_at", "license_preview", "selfie_preview")
    list_filter = ("status",)
    search_fields = ("user__username", "license_number")

    readonly_fields = ("license_preview", "selfie_preview")

    # 🔥 ADD THIS (ACTIONS)
    actions = ["approve_kyc", "reject_kyc"]

    # ✅ APPROVE ACTION
    def approve_kyc(self, request, queryset):
        queryset.update(status="approved")
    approve_kyc.short_description = "Approve selected KYC"

    # ❌ REJECT ACTION
    def reject_kyc(self, request, queryset):
        queryset.update(status="rejected")
    reject_kyc.short_description = "Reject selected KYC"

    # 🔥 License image preview
    def license_preview(self, obj):
        if obj.license_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" width="100" height="80" style="object-fit:cover;" />'
                '</a>',
                obj.license_image,
                obj.license_image
            )
        return "No Image"

    license_preview.short_description = "License"

    # 🔥 Selfie image preview
    def selfie_preview(self, obj):
        if obj.selfie_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" width="100" height="80" style="object-fit:cover;" />'
                '</a>',
                obj.selfie_image,
                obj.selfie_image
            )
        return "No Image"

    selfie_preview.short_description = "Selfie"