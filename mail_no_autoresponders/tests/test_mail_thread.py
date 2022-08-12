from email.mime.multipart import MIMEMultipart

from odoo.tests.common import TransactionCase, tagged
from odoo import models, tools


class TestMailThread(TransactionCase):
    def setUp(self):
        super(TestMailThread, self).setUp()
        # Create an email_message record with headers that we can check against

        self.message_body = {
            "body": "This is a test email",
            "subject": "Test Template",
            "email_from": "test@odoo.com",
            "author_id": self.env.user.id,
            "message_type": "email",
            "body_html": "<p>This is a test email</p>",
            "headers": {
                "X-Auto-Response-Suppress": "All",
                "X-Autoreply": "yes",
                "X-Autorespond": "yes",
                "Auto-Submitted": "no",
            },
        }
        self.mail = self.env["mail.mail"].create(self.message_body)

        self.model_mail_thread = self.env["mail.thread"]

        self.msg = MIMEMultipart()
        self.msg["From"] =  self.env.user.email
        self.msg["To"] = self.mail.email_to
        self.msg["Subject"] = "Test Template"
        self.msg["X-Autoreply"] = "yes"
        self.msg["X-Autorespond"] = "yes"
        self.msg["X-Auto-Response-Suppress"] = "All"
        self.msg["Auto-Submitted"] = "no"

        # Create a mail with auto respond headers

    def test_is_auto_response_email_message(self):
        # Check if any auto respond headers are present in the original email.
        self.mail.send()
        self.assertTrue(
            self.model_mail_thread._is_auto_response_email_message(self.mail.headers)
        )

