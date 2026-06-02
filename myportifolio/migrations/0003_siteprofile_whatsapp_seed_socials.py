from django.db import migrations, models


def seed_socials(apps, schema_editor):
    SiteProfile = apps.get_model("myportifolio", "SiteProfile")
    for profile in SiteProfile.objects.all():
        changed = False
        defaults = {
            "linkedin": "https://www.linkedin.com/",
            "instagram": "https://www.instagram.com/",
            "facebook": "https://www.facebook.com/",
            "whatsapp": "https://wa.me/254700000000",
        }
        for field, value in defaults.items():
            if not getattr(profile, field):
                setattr(profile, field, value)
                changed = True
        if changed:
            profile.save(update_fields=list(defaults.keys()))


class Migration(migrations.Migration):
    dependencies = [
        ("myportifolio", "0002_seed_portfolio_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteprofile",
            name="whatsapp",
            field=models.URLField(
                blank=True, help_text="Use a link like https://wa.me/254700000000"
            ),
        ),
        migrations.RunPython(seed_socials, migrations.RunPython.noop),
    ]
