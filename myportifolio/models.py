from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteProfile(TimestampedModel):
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=160, default="Full Stack Developer")
    tagline = models.CharField(max_length=1000000, blank=True)
    bio = models.TextField()
    profile_image = models.CharField(
        max_length=255,
        default="assets/img/hero3.jpeg",
        help_text="Static path or full URL, for example assets/img/hero3.jpeg",
    )
    hero_image = models.CharField(max_length=255, default="assets/img/hero3.jpeg")
    typed_roles = models.CharField(
        max_length=255,
        default="Developer, Designer, Freelancer",
        help_text="Comma-separated roles shown in the hero section.",
    )
    birthday = models.CharField(max_length=60, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    freelance_status = models.CharField(max_length=80, default="Available")
    address = models.CharField(max_length=255, blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    whatsapp = models.URLField(blank=True, help_text="Use a link like https://wa.me/254700000000")
    linkedin = models.URLField(blank=True)

    class Meta:
        verbose_name = "site profile"
        verbose_name_plural = "site profile"

    def __str__(self):
        return self.name


class Skill(TimestampedModel):
    name = models.CharField(max_length=80)
    proficiency = models.PositiveSmallIntegerField(default=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Education(TimestampedModel):
    degree = models.CharField(max_length=180)
    school = models.CharField(max_length=180)
    period = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.degree


class Experience(TimestampedModel):
    role = models.CharField(max_length=180)
    company = models.CharField(max_length=180)
    period = models.CharField(max_length=80)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(
        help_text="Use one responsibility per line for bullet points."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.role


class Resume(TimestampedModel):
    summary = models.TextField()
    download_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "resume"
        verbose_name_plural = "resume"

    def __str__(self):
        return "Resume"


class Service(TimestampedModel):
    title = models.CharField(max_length=120)
    icon = models.CharField(max_length=60, default="bi bi-briefcase")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Project(TimestampedModel):
    CATEGORY_CHOICES = [
        ("app", "App"),
        ("web", "Web"),
        ("branding", "Branding"),
        ("product", "Product"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="web")
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=255, default="assets/img/portfolio/app-1.jpg")
    project_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class BlogPost(TimestampedModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.CharField(max_length=255)
    content = models.TextField()
    image = models.CharField(max_length=255, default="assets/img/services.jpg")
    published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class ContactMessage(TimestampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"
