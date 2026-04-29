const API_BASE = "http://127.0.0.1:8000";

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const docList = document.getElementById("docList");
const statusEl = document.getElementById("status");
const messages = document.getElementById("messages");
const askForm = document.getElementById("askForm");
const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");
const speakToggle = document.getElementById("speakToggle");
const resetBtn = document.getElementById("resetBtn");
const convoList = document.getElementById("convoList");
const newConvoBtn = document.getElementById("newConvoBtn");

let currentConversationId = null;

function setStatus(text) {
  statusEl.textContent = text;
}

function clearEmptyState() {
  const empty = messages.querySelector(".empty");
  if (empty) empty.remove();
}

function showEmptyState() {
  messages.innerHTML =
    '<div class="empty"><h2>Upload a document to start</h2>' +
    '<p>Drop a file on the left, then ask a question below.</p></div>';
}

function appendMessage(role, text) {
  clearEmptyState();
  const node = document.createElement("div");
  node.className = `msg ${role}`;
  node.textContent = text;
  messages.appendChild(node);
  messages.scrollTop = messages.scrollHeight;
  return node;
}

function appendThinking() {
  clearEmptyState();
  const node = document.createElement("div");
  node.className = "msg bot thinking";
  node.textContent = "Thinking…";
  messages.appendChild(node);
  messages.scrollTop = messages.scrollHeight;
  return node;
}

function attachSourcesAndAudio(node, sources, audioUrl, autoplay = true) {
  node.classList.remove("thinking");
  if (sources && sources.length) {
    const wrap = document.createElement("div");
    wrap.className = "sources";
    const seen = new Set();
    sources.forEach((s) => {
      if (seen.has(s.doc)) return;
      seen.add(s.doc);
      const tag = document.createElement("span");
      const pct = Math.max(0, Math.min(100, s.score * 100));
      tag.textContent = `${s.doc} · ${pct.toFixed(0)}%`;
      wrap.appendChild(tag);
    });
    node.appendChild(wrap);
  }
  if (audioUrl) {
    const audio = document.createElement("audio");
    audio.controls = true;
    audio.src = `${API_BASE}${audioUrl}`;
    node.appendChild(audio);
    if (autoplay) audio.play().catch(() => {});
  }
}

async function refreshDocs() {
  try {
    const res = await fetch(`${API_BASE}/documents`);
    const data = await res.json();
    docList.innerHTML = "";
    if (!data.documents.length) {
      const li = document.createElement("li");
      li.className = "empty";
      li.textContent = "No documents yet.";
      docList.appendChild(li);
      return;
    }
    data.documents.forEach((name) => {
      const li = document.createElement("li");
      li.textContent = name;
      docList.appendChild(li);
    });
  } catch (err) {
    setStatus("Backend offline. Start the FastAPI server.");
  }
}

function relativeTime(unixSeconds) {
  const diff = Date.now() / 1000 - unixSeconds;
  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  if (diff < 86400 * 7) return `${Math.floor(diff / 86400)}d ago`;
  return new Date(unixSeconds * 1000).toLocaleDateString();
}

async function refreshConversations() {
  try {
    const res = await fetch(`${API_BASE}/conversations`);
    const data = await res.json();
    convoList.innerHTML = "";
    if (!data.conversations.length) {
      const li = document.createElement("li");
      li.className = "empty";
      li.textContent = "No conversations yet.";
      convoList.appendChild(li);
      return;
    }
    data.conversations.forEach((c) => {
      const li = document.createElement("li");
      li.dataset.id = c.id;
      if (c.id === currentConversationId) li.classList.add("active");

      const main = document.createElement("div");
      main.className = "convo-main";
      const title = document.createElement("span");
      title.className = "convo-title";
      title.textContent = c.title || "Untitled";
      const meta = document.createElement("span");
      meta.className = "convo-meta";
      const count = c.message_count || 0;
      meta.textContent = `${relativeTime(c.updated_at)} · ${count} msg${count === 1 ? "" : "s"}`;
      main.appendChild(title);
      main.appendChild(meta);

      const actions = document.createElement("div");
      actions.className = "convo-actions";
      const rename = document.createElement("button");
      rename.textContent = "rename";
      rename.title = "Rename conversation";
      rename.addEventListener("click", (e) => {
        e.stopPropagation();
        renameConversation(c.id, c.title);
      });
      const del = document.createElement("button");
      del.textContent = "delete";
      del.title = "Delete conversation";
      del.addEventListener("click", (e) => {
        e.stopPropagation();
        deleteConversation(c.id);
      });
      actions.appendChild(rename);
      actions.appendChild(del);

      li.appendChild(main);
      li.appendChild(actions);
      li.addEventListener("click", () => openConversation(c.id));
      convoList.appendChild(li);
    });
  } catch (err) {
    /* sidebar already shows backend status via setStatus */
  }
}

async function renameConversation(id, currentTitle) {
  const next = prompt("Rename conversation", currentTitle || "");
  if (next === null) return;
  const title = next.trim();
  if (!title) return;
  try {
    const res = await fetch(`${API_BASE}/conversations/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    if (!res.ok) throw new Error(`Rename failed (${res.status})`);
    refreshConversations();
  } catch (err) {
    setStatus(`Rename error: ${err.message}`);
  }
}

async function deleteConversation(id) {
  if (!confirm("Delete this conversation? This cannot be undone.")) return;
  try {
    const res = await fetch(`${API_BASE}/conversations/${id}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error(`Delete failed (${res.status})`);
    if (currentConversationId === id) {
      currentConversationId = null;
      showEmptyState();
    }
    refreshConversations();
  } catch (err) {
    setStatus(`Delete error: ${err.message}`);
  }
}

async function openConversation(id) {
  try {
    const res = await fetch(`${API_BASE}/conversations/${id}`);
    if (!res.ok) throw new Error(`Could not open conversation (${res.status})`);
    const data = await res.json();
    currentConversationId = data.id;
    messages.innerHTML = "";
    if (!data.messages || !data.messages.length) {
      showEmptyState();
    } else {
      data.messages.forEach((m) => {
        const role = m.role === "user" ? "user" : "bot";
        const node = appendMessage(role, m.content);
        if (role === "bot") {
          attachSourcesAndAudio(node, m.sources || [], m.audio_url, false);
        }
      });
    }
    questionInput.focus();
  } catch (err) {
    setStatus(`Open error: ${err.message}`);
  }
}

function startNewConversation() {
  currentConversationId = null;
  showEmptyState();
  questionInput.focus();
}

async function uploadFile(file) {
  setStatus(`Uploading ${file.name}…`);
  const form = new FormData();
  form.append("file", file);
  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Upload failed (${res.status})`);
    }
    const data = await res.json();
    setStatus(`Indexed ${data.filename} · ${data.chunks_added} chunks.`);
    refreshDocs();
  } catch (err) {
    setStatus(`Upload error: ${err.message}`);
  }
}

dropzone.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", (e) => {
  if (e.target.files[0]) uploadFile(e.target.files[0]);
  fileInput.value = "";
});

["dragenter", "dragover"].forEach((ev) =>
  dropzone.addEventListener(ev, (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  })
);
["dragleave", "drop"].forEach((ev) =>
  dropzone.addEventListener(ev, (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
  })
);
dropzone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files?.[0];
  if (file) uploadFile(file);
});

askForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = questionInput.value.trim();
  if (!q) return;

  appendMessage("user", q);
  questionInput.value = "";
  questionInput.style.height = "auto";
  askBtn.disabled = true;
  const thinking = appendThinking();

  try {
    const res = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: q,
        speak: speakToggle.checked,
        conversation_id: currentConversationId,
      }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Request failed (${res.status})`);
    }
    const data = await res.json();
    currentConversationId = data.conversation_id;
    thinking.textContent = data.answer;
    attachSourcesAndAudio(thinking, data.sources, data.audio_url, true);
    refreshConversations();
  } catch (err) {
    thinking.textContent = `Error: ${err.message}`;
    thinking.classList.remove("thinking");
  } finally {
    askBtn.disabled = false;
    questionInput.focus();
  }
});

questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    askForm.requestSubmit();
  }
});
questionInput.addEventListener("input", () => {
  questionInput.style.height = "auto";
  questionInput.style.height = `${Math.min(questionInput.scrollHeight, 160)}px`;
});

resetBtn.addEventListener("click", async () => {
  if (!confirm("Clear all uploaded documents and indexed data?")) return;
  setStatus("Clearing…");
  try {
    await fetch(`${API_BASE}/reset`, { method: "POST" });
    setStatus("Cleared.");
    refreshDocs();
  } catch (err) {
    setStatus(`Reset error: ${err.message}`);
  }
});

newConvoBtn.addEventListener("click", startNewConversation);

refreshDocs();
refreshConversations();
