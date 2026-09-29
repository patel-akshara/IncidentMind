import os
from hindsight_client import Hindsight

BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "incident-memory-agent")

def get_client():
    return Hindsight(
        base_url=os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"),
        api_key=os.getenv("HINDSIGHT_API_KEY"),
    )

def ensure_bank():
    client = get_client()
    try:
        client.create_bank(
            bank_id=BANK_ID,
            name="Incident Response Memory Agent",
            mission=(
                "Remember production incidents, symptoms, root causes, remediation steps, "
                "service dependencies, failed attempts, and lessons learned. Prioritize "
                "technical evidence and reusable incident-response experience."
            ),
        )
    except Exception:
        pass
    return client

def retain_incident(incident):
    client = ensure_bank()
    content = f"""
Incident: {incident['title']}
Service: {incident['service']}
Severity: {incident['severity']}
Symptoms: {incident['symptoms']}
Root cause: {incident.get('root_cause') or 'Not yet confirmed'}
Resolution: {incident.get('resolution') or 'Not yet resolved'}
"""
    client.retain(
        bank_id=BANK_ID,
        content=content,
        context="Production incident postmortem",
        metadata={"service": incident["service"], "severity": incident["severity"]},
    )

def recall_incidents(query):
    client = ensure_bank()
    result = client.recall(
        bank_id=BANK_ID,
        query=query,
        max_tokens=3000,
    )
    items = getattr(result, "results", None)
    if items is None and isinstance(result, dict):
        items = result.get("results", [])
    memories = []
    for item in items or []:
        text = getattr(item, "text", None)
        if text is None and isinstance(item, dict):
            text = item.get("text")
        if text:
            memories.append(text)
    return memories
