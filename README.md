# IncidentMind — Memory-Powered Incident Response Agent

> An AI-powered incident response assistant that learns from previous incidents using persistent Hindsight memory.

IncidentMind helps engineers investigate production incidents by combining an LLM with historical incident memory.

Instead of treating every incident as a completely new problem, IncidentMind can recall relevant past incidents, use them as evidence, and prioritize investigation steps based on previous experience.

---

## 🎯 Problem

Production incidents often repeat similar patterns.

A stateless AI assistant starts every investigation from scratch. It may analyze the current symptoms, but it does not automatically remember how similar incidents were investigated or resolved in the past.

This creates a gap:

**Past incident knowledge exists, but the AI cannot automatically use it.**

IncidentMind addresses this by giving the incident-response agent persistent memory using **Hindsight**.

---

## 💡 Solution

IncidentMind follows a continuous memory loop:

```text
                    ┌─────────────────────┐
                    │    New Incident     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    IncidentMind     │
                    │  Analyze symptoms   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Hindsight Recall  │
                    │                     │
                    │ Similar incidents   │
                    │ Previous causes     │
                    │ Previous resolutions│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Groq LLM         │
                    │  Incident Analysis  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Investigation &    │
                    │     Resolution      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Hindsight Retain   │
                    │  Store Experience   │
                    └──────────┬──────────┘
                               │
                               └──────► Future Incidents
---

## 🧠 Why Hindsight Matters

Hindsight acts as the long-term memory layer for IncidentMind.

When an incident is analyzed with memory enabled:

1. IncidentMind creates a query from the current incident.
2. Hindsight recalls relevant historical incidents.
3. The recalled incidents are provided to the LLM as historical evidence.
4. The LLM uses that evidence to prioritize investigation steps.
5. After an incident is resolved, the incident can be retained as a new memory.
6. Future incidents can benefit from the accumulated experience.

An important design principle is:

> **Historical memories are evidence, not proof.**

IncidentMind does not automatically assume that a current incident has the same root cause as a historical incident. Historical information is used to generate hypotheses that should be verified against the current system.

---

## 🔄 Before vs After Hindsight

### Without Hindsight

```text
Current Incident
       │
       ▼
     Groq
       │
       ▼
Investigation based
only on current input
```

The model only receives the current incident information.

### With Hindsight

```text
Current Incident
       │
       ▼
Hindsight Recall
       │
       ├── Similar incidents
       ├── Previous root causes
       └── Previous resolutions
       │
       ▼
     Groq
       │
       ▼
Context-aware
investigation
```

The same incident can therefore be investigated with additional historical context.

---
## 🖥️ Demo

IncidentMind demonstrates the difference using the same incident in two modes.

### 1. Analyze without memory

The incident is sent to the LLM without retrieving historical incidents.

The investigation starts from the current incident information.

### 2. Analyze with Hindsight

The same incident is analyzed with Hindsight enabled.

Hindsight recalls relevant historical incidents and provides additional context to the LLM.

The resulting investigation can use previous incidents to prioritize what should be checked first.

### 3. Retain the resolved incident

After an incident is resolved, it can be saved to Hindsight.

That experience becomes available to future investigations.

---

## 📸 Screenshots

### IncidentMind Dashboard

_Screenshot will be added here._

### Before — Memory Disabled

_Screenshot will be added here._

### After — Hindsight Memory Enabled

_Screenshot will be added here._

### Recalled Historical Incidents

_Screenshot will be added here._

---
## 🏗️ Architecture

IncidentMind uses a Flask backend that connects the user interface with SQLite, Hindsight, and Groq.

```text
                         ┌──────────────────┐
                         │     Browser      │
                         │  IncidentMind UI │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Flask API     │
                         │                  │
                         │ /api/analyze     │
                         │ /api/incidents   │
                         └────────┬─────────┘
                                  │
                   ┌──────────────┼──────────────┐
                   │              │              │
                   ▼              ▼              ▼
             ┌───────────┐  ┌────────────┐  ┌───────────┐
             │  SQLite   │  │ Hindsight  │  │   Groq    │
             │           │  │            │  │           │
             │ Incident  │  │ Long-term  │  │    LLM    │
             │ history   │  │  memory    │  │ analysis  │
             └───────────┘  └─────┬──────┘  └─────┬─────┘
                                  │                │
                                  └───────┬────────┘
                                          │
                                          ▼
                                  Incident Analysis
```

### Components

| Component | Purpose |
|---|---|
| **Flask** | Backend API and web application |
| **SQLite** | Stores application incident history |
| **Hindsight** | Persistent agent memory |
| **Groq** | LLM-based incident analysis |
| **HTML/CSS/JavaScript** | Frontend dashboard |
| **Python** | Application logic |

---

## 🛠️ Tech Stack

- Python
- Flask
- SQLite
- Hindsight
- Groq
- HTML
- CSS
- JavaScript

The project does not require Node.js, React, XAMPP, MySQL, or Docker.

---
## 📁 Project Structure

```text
IncidentMind/
│
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── llm.py
│   ├── memory.py
│   ├── routes.py
│   │
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   │
│   └── templates/
│       └── index.html
│
├── data/
│   └── seed_incidents.json
│
├── docs/
│   ├── architecture.md
│   ├── demo-script.md
│   ├── article.md
│   └── linkedin.md
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
└── start_windows.bat
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- Groq API key
- Hindsight API key

### 1. Clone the repository

```bash
git clone https://github.com/patel-akshara/IncidentMind.git
cd IncidentMind
```

### 2. Create a virtual environment

On Windows:

```powershell
py -3 -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Create the environment file

```powershell
copy .env.example .env
```

### 6. Add your API keys

Open `.env` and add your own credentials:

```text
FLASK_SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
HINDSIGHT_API_KEY=your-hindsight-api-key
```

Keep `.env` private.

**Never commit API keys to GitHub.**

### 7. Start the application

```powershell
python run.py
```

The application will start at:

```text
http://127.0.0.1:5000
```

Open that address in your browser.

---

## 🔐 Environment Variables

IncidentMind uses environment variables for external services.

The available configuration is:

```text
FLASK_SECRET_KEY=
GROQ_API_KEY=
HINDSIGHT_API_KEY=
HINDSIGHT_BASE_URL=
HINDSIGHT_BANK_ID=
GROQ_MODEL=
```

A safe template is provided in:

```text
.env.example
```

The actual `.env` file is excluded from Git using `.gitignore`.

---
## 🧪 Example Incident

The project includes sample incidents involving checkout API latency and database performance.

Example:

```text
Title:
Checkout API latency after database deployment

Service:
Checkout API

Severity:
High

Symptoms:
Checkout requests are taking significantly longer than normal
after a database deployment.
```

With Hindsight enabled, IncidentMind can recall related historical incidents.

For example, a previous incident involving a missing composite index may become a hypothesis to investigate.

The system does not automatically assume that the current incident has the same root cause.

---

## 🔁 Memory Workflow

### Retain

When an incident is resolved, relevant information can be stored in Hindsight.

```text
Resolved Incident
       │
       ▼
Hindsight Retain
       │
       ▼
Persistent Memory
```

### Recall

When a new incident arrives:

```text
New Incident
     │
     ▼
Hindsight Recall
     │
     ▼
Relevant Historical Incidents
     │
     ▼
Groq Analysis
```

This creates a continuous learning loop across incidents.

---
## 🛡️ Safety and Reliability

IncidentMind is designed to distinguish between:

- Current observations
- Historical evidence
- Hypotheses
- Verification steps
- Recommended actions

Historical memory is treated as **evidence, not proof**.

The AI is instructed not to invent:

- Logs
- Metrics
- Configurations
- Database states
- Deployments
- Confirmed root causes

Potentially disruptive actions such as database changes, rollbacks, restarts, or configuration changes should be verified before execution.

---

## ⚠️ Current Limitations

IncidentMind is a prototype and has several limitations:

- Historical memories still need to be verified against the current system.
- Investigation quality depends on the information provided about the incident.
- The system does not directly access production infrastructure, logs, metrics, or databases.
- LLM-generated investigation steps should be reviewed by an engineer before execution.
- Hindsight and Groq require valid API credentials and network access.

---

## 🔮 Future Improvements

Possible future extensions include:

- Integration with real monitoring systems
- Log and metric retrieval
- Slack or incident-management integration
- Automatic postmortem generation
- Incident severity classification
- Runbook retrieval
- Timeline generation
- Advanced incident similarity analysis
- Team-specific operational memory

---
## 🎥 Demo Flow

A short demonstration can follow this sequence:

```text
1. Open IncidentMind
          ↓
2. Enter a production incident
          ↓
3. Analyze WITHOUT memory
          ↓
4. Show the absence of historical context
          ↓
5. Analyze WITH Hindsight
          ↓
6. Show recalled historical incidents
          ↓
7. Compare the investigation plans
          ↓
8. Resolve and retain the incident
          ↓
9. Explain how future incidents can use the new memory
```

---

## 📌 Key Takeaway

IncidentMind demonstrates how persistent agent memory can change an AI incident-response workflow.

Instead of:

```text
"Analyze this incident from scratch."
```

the workflow becomes:

```text
"Analyze this incident using relevant experience
from previous incidents, while still verifying
the current system."
```

Hindsight provides the persistent memory layer that makes this workflow possible.

---

## 🔗 Resources

- GitHub: https://github.com/patel-akshara/IncidentMind
- Hindsight GitHub: https://github.com/vectorize-io/hindsight
- Hindsight Documentation: https://hindsight.vectorize.io/
- Groq: https://groq.com/

---

## 👩‍💻 Author

**Akshara Patel**

B.Tech — Computer Science & Engineering (Data Science)

---

## 📄 License

This project is intended for educational and demonstration purposes.s