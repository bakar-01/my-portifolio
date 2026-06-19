import logging

from django.contrib import messages
from django.db import DatabaseError
from django.http import Http404
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

logger = logging.getLogger(__name__)


def _fallback_profile():
    return SiteProfile(
        name="Bakari Tungwa Bakari",
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


def _site_profile():
    profile = SiteProfile.objects.order_by("-updated_at").first()
    if profile:
        return profile

    return _fallback_profile()


def index(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except DatabaseError:
                logger.exception("Failed to save contact message.")
                messages.error(
                    request,
                    "Sorry, your message couldn't be sent right now. Please try again later.",
                )
            else:
                messages.success(request, "Your message has been sent. Thank you!")
                return redirect("index")
        else:
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
    post = get_object_or_404(
        BlogPost,
        slug=slug,
        published=True,
    )
    if post.published_at and post.published_at > timezone.now():
        raise Http404("Blog post not found.")
    return render(
        request,
        "blog_detail.html",
        {"profile": _site_profile(), "post": post},
    )


def _error_context(status_code, page_title, headline, message):
    return {
        "profile": _fallback_profile(),
        "status_code": status_code,
        "page_title": page_title,
        "headline": headline,
        "message": message,
    }


def bad_request(request, exception):
    return render(
        request,
        "error.html",
        _error_context(
            400,
            "Bad Request",
            "That request could not be processed.",
            "The browser sent something the site could not understand. Try refreshing the page or head back home.",
        ),
        status=400,
    )


def permission_denied(request, exception):
    return render(
        request,
        "error.html",
        _error_context(
            403,
            "Access Denied",
            "This page is not available.",
            "You do not have permission to view this part of the site.",
        ),
        status=403,
    )


def page_not_found(request, exception):
    return render(
        request,
        "error.html",
        _error_context(
            404,
            "Page Not Found",
            "I could not find that page.",
            "The link may be outdated, or the page may have moved. You can return home and keep browsing the portfolio.",
        ),
        status=404,
    )


def server_error(request):
    return render(
        request,
        "error.html",
        _error_context(
            500,
            "Server Error",
            "Something went wrong.",
            "The site hit an unexpected issue. Please try again in a moment.",
        ),
        status=500,
    )
