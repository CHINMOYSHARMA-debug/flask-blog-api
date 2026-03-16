from flask import Blueprint, jsonify
from app.extensions import db
from sqlalchemy import text
import redis
import os

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    status={
        "api": "ok",
        "database": "unknown",
        "redis": "unknown"
    }

    try:
        db.session.execute(text("SELECT 1"))
        status["database"] = "ok"
    except Exception:
        status["database"] = "error"

    try:
        r = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))
        r.ping()
        status["redis"] = "ok"
    except Exception:
        status["redis"] = "error"

    overall = "healthy" if all(v == "ok" for v in status.values()) else "degraded"

    return jsonify({
        "status": overall,
        "services": status
    })
