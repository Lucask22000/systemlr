from flask import jsonify


def ok(data=None, message="OK", *, code="ok", status=200, action=None):
    payload = {
        "success": True,
        "message": message,
        "code": code,
        "data": data if data is not None else {},
    }
    if action:
        payload["action"] = action
    return jsonify(payload), status


def fail(message, *, code="request_failed", status=400, fields=None, action=None):
    payload = {
        "success": False,
        "message": message,
        "code": code,
        "fields": fields or {},
    }
    if action:
        payload["action"] = action
    return jsonify(payload), status
