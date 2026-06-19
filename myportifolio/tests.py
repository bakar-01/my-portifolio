from datetime import timedelta
from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import BlogPost


TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


@override_settings(
    DEBUG=False,
    ALLOWED_HOSTS=["testserver"],
    STORAGES=TEST_STORAGES,
)
class ErrorHandlingTests(TestCase):
    def test_missing_page_uses_custom_404_template(self):
        response = self.client.get("/missing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Error 404", status_code=404)
        self.assertContains(response, "I could not find that page.", status_code=404)

    def test_future_blog_post_returns_404(self):
        post = BlogPost.objects.create(
            title="Future Post",
            excerpt="This should stay unpublished until its scheduled date.",
            content="Coming soon.",
            published=True,
            published_at=timezone.now() + timedelta(days=1),
        )

        response = self.client.get(reverse("blog_detail", kwargs={"slug": post.slug}))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Error 404", status_code=404)

    def test_contact_save_failure_shows_friendly_message(self):
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Website inquiry",
            "message": "Hello from the test suite.",
        }

        with self.assertLogs("myportifolio.views", level="ERROR"):
            save_patch = patch(
                "myportifolio.forms.ContactMessageForm.save",
                side_effect=DatabaseError,
            )
            with save_patch:
                response = self.client.post(reverse("index"), form_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "message couldn", status_code=200)
        self.assertContains(response, "sent right now", status_code=200)
