# IncidentMind — Memory-Powered Incident Response Agent

IncidentMind is an AI incident-response assistant built around **Hindsight agent memory**.

## Problem
Production incidents often repeat patterns. A stateless chatbot starts from scratch every time. IncidentMind stores resolved incidents in Hindsight and recalls relevant experience for the next incident.

## Architecture

```text
Browser -> Flask API -> SQLite (dashboard history)
                  |
                  +-> Hindsight: retain / recall
                  |
                  +-> Groq: incident analysis using recalled memory
```

SQLite is the application log. **Hindsight is the agent's long-term memory layer.**

## Setup

Python 3.10+.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Open http://127.0.0.1:5000

Put your Groq and Hindsight API keys in `.env`.

## Demo
1. Save the three sample incidents in `data/seed_incidents.json` through the UI.
2. Use the default checkout latency incident.
3. Click **Analyze without memory**.
4. Click **Analyze with Hindsight** on the same incident.
5. Compare the response and the recalled-memory panel.
6. Save the resolved incident to create another memory.

## Why this fits the challenge
- Real professional workflow: incident response.
- Persistent memory is central.
- Clear before/after behavior.
- Memory improves over repeated incidents.
- The agent treats recalled incidents as evidence, not certainty.
