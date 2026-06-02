from django.contrib import admin

from .models import (
    BlogPost,
    ContactMessage,
    Education,
    Experience,
    Project,
    Resume,
    Service,
    SiteProfile,
    Skill,
)


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "phone", "updated_at")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "proficiency", "order")
    list_editable = ("proficiency", "order")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "school", "period", "order")
    list_editable = ("order",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "period", "order")
    list_editable = ("order",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "download_url", "updated_at")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "order", "updated_at")
    list_editable = ("is_featured", "order")
    list_filter = ("category", "is_featured")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "description")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "published_at", "updated_at")
    list_editable = ("published",)
    list_filter = ("published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt", "content")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at", "updated_at")
