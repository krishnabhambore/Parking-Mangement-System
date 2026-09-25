const $ = (id) => document.getElementById(id);
let slots = [], selected = null;

const api = async (url, opts) => {
  const res = await fetch(url, opts);
  return { ok: res.ok, data: await res.json() };
};
const toast = (msg, ok) => { const t = $("toast"); t.textContent = msg; t.className = ok ? "ok" : "err"; };
const fmt = (iso) => new Date(iso).toLocaleString([], { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });

function renderSlots() {
  for (const type of ["bike", "car"]) {
    $("bays-" + type).innerHTML = "";
    slots.filter((s) => s.type === type).forEach((s) => {
      const b = document.createElement("button");
      b.className = "bay " + (s.ticket_id ? "taken" : "free") + (selected === s.ticket_id && s.ticket_id ? " sel" : "");
      b.innerHTML = `<span class="label">${s.label}</span><span class="plate">${s.plate || "Free"}</span>`;
      b.disabled = !s.ticket_id;
      b.onclick = () => { selected = s.ticket_id; renderSlots(); renderDetail(); };
      $("bays-" + type).appendChild(b);
    });
  }
  const taken = slots.filter((s) => s.ticket_id).length;
  $("stats").innerHTML = `<span><b>${slots.length - taken}</b>free</span><span><b>${taken}</b>occupied</span>`;
}

function renderDetail() {
  const s = selected ? slots.find((x) => x.ticket_id === selected) : null, d = $("detail");
  if (!s) { d.hidden = true; return; }
  d.hidden = false;
  d.innerHTML = `<h2>Bay ${s.label}</h2><p><b>${s.plate}</b></p><p>Entered ${fmt(s.entry_time)}</p>
    <button id="out">Check out and bill</button>`;
  $("out").onclick = async () => {
    const r = await api("/api/exit/" + s.ticket_id, { method: "POST" });
    toast(r.data.message || r.data.error, r.ok);
    selected = null; refresh();
  };
}

async function refresh() {
  slots = (await api("/api/slots")).data;
  renderSlots(); renderDetail();
  const h = (await api("/api/history")).data;
  if (h.rows.length) {
    $("history").innerHTML = h.rows.map((r) =>
      `<tr><td>${r.plate}</td><td>${r.bay}</td><td>${fmt(r.entry_time)}</td><td>${fmt(r.exit_time)}</td><td>₹${r.fee}</td></tr>`).join("");
  }
  $("stats").innerHTML += `<span><b>₹${h.revenue_today}</b>collected today</span>`;
}

$("park-form").onsubmit = async (e) => {
  e.preventDefault();
  const r = await api("/api/park", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plate: $("plate").value, type: $("type").value }),
  });
  toast(r.data.message || r.data.error, r.ok);
  if (r.ok) $("plate").value = "";
  refresh();
};

refresh();
setInterval(refresh, 30000);