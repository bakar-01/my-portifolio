from datetime import timedelta
from unittest.mock import patch

from django.core import mail
from django.db import DatabaseError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import BlogPost, ContactMessage


TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


@override_settings(
    DEBUG=False,
    ALLOWED_HOSTS=["testserver"],
    CONTACT_NOTIFICATION_RECIPIENTS=["admin@example.com"],
    DEFAULT_FROM_EMAIL="portfolio@example.com",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
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

    def test_contact_form_notifies_admin_after_message_is_saved(self):
        form_data = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "subject": "Project inquiry",
            "message": "I would like to talk about a new website.",
        }

        response = self.client.post(reverse("index"), form_data)

        self.assertRedirects(response, reverse("index"), fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

        notification = mail.outbox[0]
        self.assertIn("admin@example.com", notification.to)
        self.assertEqual(notification.reply_to, ["ada@example.com"])
        self.assertIn("New portfolio contact: Project inquiry", notification.subject)
        self.assertIn("Ada Lovelace", notification.body)
        self.assertIn("View this message in Django admin", notification.body)

    def test_contact_notification_failure_does_not_block_submission(self):
        form_data = {
            "name": "Grace Hopper",
            "email": "grace@example.com",
            "subject": "Hello",
            "message": "Checking whether the form still works.",
        }

        send_patch = patch(
            "myportifolio.views.EmailMessage.send",
            side_effect=RuntimeError("mail server unavailable"),
        )
        with self.assertLogs("myportifolio.views", level="ERROR"):
            with send_patch:
                response = self.client.post(reverse("index"), form_data)

        self.assertRedirects(response, reverse("index"), fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 1)
