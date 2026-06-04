import json
from unittest.mock import Mock, patch

from django.test import TestCase


class MessageApiTests(TestCase):
    @patch("api.views.OpenAI")
    def test_message_returns_openai_response(self, mock_openai):
        mock_client = Mock()
        mock_client.responses.create.return_value.output_text = "openai response"
        mock_openai.return_value = mock_client

        with self.settings(OPENAI_API_KEY="test-key", OPENAI_MODEL="test-model"):
            response = self.client.post(
                "/api/message/",
                data=json.dumps({"text": "hello"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True, "message": "openai response"})
        mock_openai.assert_called_once_with(api_key="test-key")
        mock_client.responses.create.assert_called_once_with(model="test-model", input="hello")

    def test_message_requires_openai_api_key(self):
        response = self.client.post(
            "/api/message/",
            data=json.dumps({"text": "hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"ok": False, "error": "OPENAI_API_KEY is not configured"})

    def test_message_rejects_non_string_text(self):
        response = self.client.post(
            "/api/message/",
            data=json.dumps({"text": 123}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
