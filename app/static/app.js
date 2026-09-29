function payload(){
  return {
    title: document.getElementById("title").value,
    service: document.getElementById("service").value,
    severity: document.getElementById("severity").value,
    symptoms: document.getElementById("symptoms").value
  };
}

async function analyze(useMemory){
  const p = payload();
  document.getElementById("resultTitle").textContent = p.title;
  document.getElementById("answer").textContent = "Analyzing…";
  document.getElementById("memories").textContent = "Retrieving memory…";
  document.getElementById("memoryBadge").textContent = useMemory ? "HINDSIGHT ON" : "MEMORY OFF";

  const r = await fetch("/api/analyze", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body:JSON.stringify({...p,use_memory:useMemory})
  });
  const data = await r.json();
  if(!r.ok){ document.getElementById("answer").textContent = data.error || "Request failed"; return; }

  document.getElementById("answer").textContent = data.answer;
  document.getElementById("memoryCount").textContent = `${data.memory_count} memories`;
  const box = document.getElementById("memories");
  box.innerHTML = data.memories.length
    ? data.memories.map(x=>`<div class="memory-item">${escapeHtml(x)}</div>`).join("")
    : "No relevant historical memories were retrieved.";
}

async function saveIncident(){
  const p = payload();
  p.root_cause = document.getElementById("root_cause").value;
  p.resolution = document.getElementById("resolution").value;
  const r = await fetch("/api/incidents", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body:JSON.stringify(p)
  });
  const data = await r.json();
  document.getElementById("saveStatus").textContent =
    r.ok ? `Saved. Hindsight status: ${data.memory_status}` : (data.error || "Save failed");
  loadHistory();
}

async function loadHistory(){
  const r = await fetch("/api/incidents");
  const rows = await r.json();
  const el = document.getElementById("historyList");
  el.innerHTML = rows.length ? rows.map(x=>`
    <div class="incident-row">
      <span class="pill">${escapeHtml(x.severity)}</span>
      <strong>${escapeHtml(x.title)}</strong>
      <span>${escapeHtml(x.service)}</span>
      <span>${escapeHtml(x.root_cause || "Unresolved")}</span>
    </div>`).join("") : "<p class='muted'>No incidents saved yet.</p>";
}

function escapeHtml(s){
  return String(s ?? "").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[m]));
}
loadHistory();
