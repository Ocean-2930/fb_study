import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from openai import OpenAI


def with_cors(request, response):
    origin = request.headers.get("Origin")
    if origin in settings.CORS_ALLOWED_ORIGINS:
        response["Access-Control-Allow-Origin"] = origin
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Accept"
    return response


def ping(request):
    return with_cors(request, JsonResponse({"ok": True, "message": "pong"}))


@csrf_exempt
def message(request):
    if request.method == "OPTIONS":
        return with_cors(request, JsonResponse({}))

    if request.method != "POST":
        return with_cors(request, JsonResponse({"ok": False, "error": "POST required"}, status=405))

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return with_cors(request, JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400))

    text = payload.get("text", "")
    if not isinstance(text, str):
        return with_cors(request, JsonResponse({"ok": False, "error": "text must be a string"}, status=400))

    if not settings.OPENAI_API_KEY:
        return with_cors(
            request,
            JsonResponse({"ok": False, "error": "OPENAI_API_KEY is not configured"}, status=500),
        )

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=text,
    ).output_text

    return with_cors(request, JsonResponse({"ok": True, "message": response}))
