from time import sleep

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

SLOW_RESPONSE_SECONDS = 80


def text_field(payload, field):
    if not isinstance(payload, dict):
        raise ValidationError("Expected a JSON object.")
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip() or len(value) > 5000:
        raise ValidationError(f"'{field}' must be a nonempty string of at most 5000 characters.")
    return value


@api_view(["GET"])
def health(_request):
    return Response({"status": "ok"})


@api_view(["GET"])
def info(_request):
    return Response({"framework": "django", "profile": "light"})


@api_view(["POST"])
def echo(request):
    message = text_field(request.data, "message")
    count = request.data.get("count")
    if not isinstance(count, int) or isinstance(count, bool):
        raise ValidationError("'count' must be an integer.")
    return Response({"received": {"message": message, "count": count}})


@api_view(["GET"])
def item(request, item_id):
    raw = request.query_params.get("include_details", "false").lower()
    if item_id < 1 or raw not in {"true", "false"}:
        raise ValidationError("Expected a positive item ID and true/false include_details.")
    result = {"item_id": item_id, "include_details": raw == "true"}
    if result["include_details"]:
        result["details"] = f"Reference item {item_id}"
    return Response(result)


@api_view(["GET"])
def slow(_request):
    sleep(SLOW_RESPONSE_SECONDS)
    return Response({"delay_seconds": SLOW_RESPONSE_SECONDS, "status": "completed"})
