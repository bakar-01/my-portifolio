from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify


def seed_content(apps, schema_editor):
    SiteProfile = apps.get_model("myportifolio", "SiteProfile")
    Skill = apps.get_model("myportifolio", "Skill")
    Education = apps.get_model("myportifolio", "Education")
    Experience = apps.get_model("myportifolio", "Experience")
    Resume = apps.get_model("myportifolio", "Resume")
    Service = apps.get_model("myportifolio", "Service")
    Project = apps.get_model("myportifolio", "Project")
    BlogPost = apps.get_model("myportifolio", "BlogPost")

    SiteProfile.objects.get_or_create(
        name="Bakari Tungwa",
        defaults={
            "title": "Full Stack Django Developer",
            "tagline": "Responsive portfolio websites, business apps, and database-backed web systems.",
            "bio": "I build clean, responsive web experiences with Django, Bootstrap, JavaScript, and practical admin workflows that make content easy to manage.",
            "profile_image": "assets/img/hero3.jpeg",
            "hero_image": "assets/img/hero3.jpeg",
            "typed_roles": "Django Developer, Web Designer, Freelancer, Problem Solver",
            "website": "https://example.com",
            "phone": "+254 700 000 000",
            "city": "Nairobi, Kenya",
            "degree": "Software Engineering",
            "email": "hello@example.com",
            "freelance_status": "Available",
            "address": "Nairobi, Kenya",
        },
    )

    for order, (name, proficiency) in enumerate(
        [
            ("HTML", 95),
            ("CSS", 90),
            ("JavaScript", 82),
            ("Python", 88),
            ("Django", 90),
            ("Bootstrap", 86),
        ],
        start=1,
    ):
        Skill.objects.get_or_create(
            name=name, defaults={"proficiency": proficiency, "order": order}
        )

    Education.objects.get_or_create(
        degree="Software Engineering",
        school="Portfolio Academy",
        period="2022 - 2025",
        defaults={
            "description": "Focused on web development, databases, software design, and deployment.",
            "order": 1,
        },
    )

    Experience.objects.get_or_create(
        role="Django Developer",
        company="Freelance",
        period="2024 - Present",
        defaults={
            "location": "Remote",
            "description": "Build responsive portfolio and business websites.\nCreate database-backed admin dashboards.\nIntegrate contact forms, blogs, and project galleries.",
            "order": 1,
        },
    )

    Resume.objects.get_or_create(
        defaults={
            "summary": "Developer experienced in building responsive Django websites with dynamic portfolio, blog, services, resume, and contact-management features."
        }
    )

    for order, (title, icon, description) in enumerate(
        [
            (
                "Django Web Development",
                "bi bi-code-slash",
                "Custom websites and web apps with clean models, admin management, and maintainable views.",
            ),
            (
                "Responsive UI Design",
                "bi bi-phone",
                "Mobile-friendly Bootstrap layouts that work smoothly across phones, tablets, and desktops.",
            ),
            (
                "Portfolio Setup",
                "bi bi-kanban",
                "Dynamic project galleries, resume pages, blogs, and contact workflows for personal brands.",
            ),
        ],
        start=1,
    ):
        Service.objects.get_or_create(
            title=title,
            defaults={
                "icon": icon,
                "description": description,
                "order": order,
                "is_active": True,
            },
        )

    for order, project in enumerate(
        [
            {
                "title": "Dynamic Portfolio Website",
                "category": "web",
                "short_description": "A Django-powered portfolio with admin-managed projects, services, resume, and blog posts.",
                "description": "Built with Django models, Bootstrap, responsive sections, detail pages, and a database-backed contact form.",
                "image": "assets/img/portfolio/app-1.jpg",
                "is_featured": True,
            },
            {
                "title": "Business Landing System",
                "category": "product",
                "short_description": "A content-managed business website for services, leads, and project showcases.",
                "description": "Designed for easy updates from Django admin and a polished responsive customer experience.",
                "image": "assets/img/portfolio/product-1.jpg",
                "is_featured": True,
            },
            {
                "title": "Brand Portfolio Gallery",
                "category": "branding",
                "short_description": "A filterable gallery for visual work, case studies, and brand assets.",
                "description": "Uses category filters, project detail links, and responsive image cards.",
                "image": "assets/img/portfolio/branding-1.jpg",
                "is_featured": False,
            },
        ],
        start=1,
    ):
        Project.objects.get_or_create(
            title=project["title"],
            defaults={**project, "slug": slugify(project["title"]), "order": order},
        )

    BlogPost.objects.get_or_create(
        title="Building a Dynamic Django Portfolio",
        defaults={
            "slug": "building-a-dynamic-django-portfolio",
            "excerpt": "How a database-backed portfolio keeps your content fresh without editing templates.",
            "content": "A dynamic portfolio lets you update projects, services, resume entries, and blog posts directly from Django admin. That keeps the website maintainable while preserving a polished public experience.",
            "image": "assets/img/services.jpg",
            "published": True,
            "published_at": timezone.now(),
        },
    )


def unseed_content(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("myportifolio", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_content, unseed_content),
    ]
