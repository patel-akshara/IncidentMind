from flask import Blueprint, jsonify, render_template, request, current_app
from .db import insert_incident, list_incidents
from .memory import retain_incident, recall_incidents
from .llm import analyze_incident

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/api/incidents")
def incidents():
    return jsonify(list_incidents(current_app.config["DATABASE"]))


@bp.post("/api/incidents")
def create_incident():
    data = request.get_json(force=True)

    required = ["title", "service", "severity", "symptoms"]
    missing = [x for x in required if not data.get(x)]

    if missing:
        return jsonify({
            "error": f"Missing: {', '.join(missing)}"
        }), 400

    incident = {
        k: data.get(k)
        for k in [
            "title",
            "service",
            "severity",
            "symptoms",
            "root_cause",
            "resolution"
        ]
    }

    incident_id = insert_incident(
        current_app.config["DATABASE"],
        incident
    )

    incident["id"] = incident_id

    try:
        retain_incident(incident)
        memory_status = "stored"
    except Exception as exc:
        memory_status = f"memory_error: {type(exc).__name__}"

    return jsonify({
        "incident": incident,
        "memory_status": memory_status
    }), 201


@bp.post("/api/analyze")
def analyze():
    data = request.get_json(force=True)

    required = ["title", "service", "severity", "symptoms"]
    missing = [x for x in required if not data.get(x)]

    if missing:
        return jsonify({
            "error": f"Missing: {', '.join(missing)}"
        }), 400

    incident = {
        k: data.get(k)
        for k in [
            "title",
            "service",
            "severity",
            "symptoms",
            "root_cause",
            "resolution"
        ]
    }

    use_memory = bool(data.get("use_memory", True))

    memories = []
    if use_memory:
        try:
            query = (
                f"{incident['service']} "
                f"{incident['title']} "
                f"{incident['symptoms']}"
            )

            memories = recall_incidents(query)

        except Exception as exc:
            print(
                f"HINDSIGHT RECALL ERROR: "
                f"{type(exc).__name__}: {exc}"
            )

            return jsonify({
                "error": (
                    f"Hindsight recall failed: "
                    f"{type(exc).__name__}: {exc}"
                )
            }), 502
    try:
        answer = analyze_incident(
            incident,
            memories
        )

    except Exception as exc:
        print(
            f"LLM ERROR: "
            f"{type(exc).__name__}: {exc}"
        )

        return jsonify({
            "error": (
                f"LLM request failed: "
                f"{type(exc).__name__}: {exc}"
            )
        }), 502

    # Temporary debugging output
    print("========== AI ANSWER ==========")
    print(answer)
    print("========== END AI ANSWER ==========")

    return jsonify({
        "answer": answer,
        "memories": memories,
        "memory_used": use_memory,
        "memory_count": len(memories),
    })