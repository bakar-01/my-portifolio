from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ContactMessageForm
from .models import (
    BlogPost,
    Education,
    Experience,
    Project,
    Resume,
    Service,
    SiteProfile,
    Skill,
)


def _site_profile():
    profile = SiteProfile.objects.order_by("-updated_at").first()
    if profile:
        return profile

    return SiteProfile(
        name="Bakari Tungwa",
        title="Full Stack Developer",
        tagline="I build responsive web experiences and database-backed products.",
        bio=(
            "A creative developer focused on clean interfaces, reliable Django "
            "backends, and practical digital products."
        ),
        email="hello@example.com",
        phone="+254 700 000 000",
        city="Nairobi, Kenya",
        degree="Software Engineering",
        website="https://example.com",
    )


def index(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent. Thank you!")
            return redirect("index")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = ContactMessageForm()

    posts = BlogPost.objects.filter(published=True).filter(
        published_at__lte=timezone.now()
    ) | BlogPost.objects.filter(published=True, published_at__isnull=True)

    context = {
        "profile": _site_profile(),
        "skills": Skill.objects.all(),
        "education": Education.objects.all(),
        "experience": Experience.objects.all(),
        "resume": Resume.objects.order_by("-updated_at").first(),
        "services": Service.objects.filter(is_active=True),
        "projects": Project.objects.all(),
        "featured_projects": Project.objects.filter(is_featured=True),
        "blog_posts": posts.distinct()[:3],
        "contact_form": form,
    }
    return render(request, "index.html", context)


def resume_page(request):
    context = {
        "profile": _site_profile(),
        "resume": Resume.objects.order_by("-updated_at").first(),
        "education": Education.objects.all(),
        "experience": Experience.objects.all(),
        "skills": Skill.objects.all(),
    }
    return render(request, "resume.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(
        request,
        "project_detail.html",
        {"profile": _site_profile(), "project": project},
    )


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(
        request,
        "blog_detail.html",
        {"profile": _site_profile(), "post": post},
    )
