import os
from groq import Groq
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
def analyze_incident(incident, memories):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    memory_text = (
        "\n".join(f"- {m}" for m in memories)
        if memories
        else "No relevant historical incidents were retrieved."
    )
    system = """You are an incident response engineer.

Analyze production incidents conservatively and distinguish observed facts
from historical evidence and hypotheses.

Important rules:
- Never invent logs, metrics, commands, configurations, deployments,
  database states, or confirmed root causes.
- Treat historical memories as evidence and useful clues, NOT as proof that
  the current incident has the same root cause.
- Before recommending a change, first recommend verifying the current system
  state.
- Never state that a historical root cause is confirmed for the current
  incident unless the current incident provides direct evidence.
- When historical memory suggests a possible cause, explicitly say that it
  is a hypothesis to verify.
- Prefer safe investigation steps before potentially disruptive actions such
  as database changes, rollbacks, restarts, or configuration changes.
- Do not claim that a mitigation succeeded unless the current incident
  provides evidence that it succeeded.
- Clearly distinguish between observed symptoms, historical context,
  hypotheses, verification steps, and recommended actions.

Return:
1. Initial assessment
2. Similar historical incidents
3. Recommended investigation steps
4. Likely causes with confidence labels
5. Immediate mitigation
6. What to record for future incidents

Keep the response practical, technically specific, and concise."""
    user = f"""CURRENT INCIDENT
Title: {incident['title']}
Service: {incident['service']}
Severity: {incident['severity']}
Symptoms: {incident['symptoms']}
HISTORICAL MEMORY
{memory_text}
Explain how the historical memory changes your investigation plan.
Important:
- Do not assume the current incident has the same root cause as a historical
  incident.
- Use historical incidents to prioritize what should be investigated.
- Clearly identify what must be verified in the current system.
- If there is no useful historical memory, say so."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            }
        ],
        temperature=0.2,
        max_tokens=1200,
    )
    return response.choices[0].message.content