# I Built an Incident Agent That Remembers What Production Taught Us

Production incidents are rarely unique. The frustrating part is that the useful information from the last incident is often trapped in a postmortem, a ticket, or someone's memory.

I built IncidentMind around a simple idea: an incident-response agent should accumulate experience.

## What the system does

IncidentMind accepts a production incident containing the service, severity, and symptoms. It produces an investigation plan.

Before the language model writes that plan, the application asks Hindsight for relevant historical memory.

Resolved incidents are stored with `retain()`. New incidents use `recall()` to retrieve relevant experience. The retrieved memories are passed to the language model as evidence.

```text
incident -> recall history -> investigate -> resolve -> retain learning
```

## Why memory changes the workflow

Without memory, an incident agent can still produce a reasonable checklist. It can mention logs, metrics, deployments, database queries, and dependencies.

But it has no experience.

If checkout latency jumps after a database deployment, a stateless model sees only those symptoms. With Hindsight, the agent can retrieve an earlier checkout incident involving a similar database slowdown.

That does not prove the current root cause. It changes the investigation order.

## The memory layer

The integration is intentionally small:

```python
client.retain(
    bank_id=BANK_ID,
    content=content,
    context="Production incident postmortem",
)
```

A new incident becomes a recall query:

```python
result = client.recall(
    bank_id=BANK_ID,
    query=f"{service} {title} {symptoms}",
    max_tokens=3000,
)
```

Hindsight provides the long-term memory layer while SQLite remains the local application log.

## The before/after demo

The UI has two buttons:

**Analyze without memory**

**Analyze with Hindsight**

The first sends no historical incidents to the model. The second retrieves relevant memories.

This makes memory visible instead of hiding it as an implementation detail.

## What I learned

### 1. Memory needs a job
A memory system matters when it changes a real decision. Here, historical incidents change the investigation plan.

### 2. Store outcomes
Symptoms plus root cause plus resolution are more useful than an arbitrary chat transcript.

### 3. Similarity is not certainty
A recalled incident is evidence, not proof. The agent must still verify the current system.

### 4. Expose the learning loop
The strongest demo is:

```text
incident -> recall -> recommendation -> resolution -> new memory
```

## Next step

A production version could connect incident-management systems, deployment history, logs, and postmortems so the memory bank becomes a durable source of organizational incident experience.
