const presets = {
  baseline: {
    subject_id: "demo-subject-01",
    context: "general",
    signals: {
      eeg_focus_index: 72,
      theta_beta_ratio: 1.8,
      blink_rate_per_min: 14,
      hrv_rmssd: 58,
      typing_speed_wpm: 54,
      typing_error_rate: 0.06,
      mouse_hesitation_score: 28,
      task_switches_per_min: 6,
      session_duration_min: 42
    }
  },
  "coding-crunch": {
    subject_id: "developer-ops-07",
    context: "coding",
    signals: {
      eeg_focus_index: 46,
      theta_beta_ratio: 3.2,
      blink_rate_per_min: 24,
      hrv_rmssd: 24,
      typing_speed_wpm: 38,
      typing_error_rate: 0.17,
      mouse_hesitation_score: 62,
      task_switches_per_min: 15,
      session_duration_min: 118
    }
  },
  "exam-overload": {
    subject_id: "student-eval-02",
    context: "exam",
    signals: {
      eeg_focus_index: 39,
      theta_beta_ratio: 3.8,
      blink_rate_per_min: 29,
      hrv_rmssd: 18,
      typing_speed_wpm: 31,
      typing_error_rate: 0.22,
      mouse_hesitation_score: 71,
      task_switches_per_min: 18,
      session_duration_min: 132
    }
  }
};

const form = document.getElementById("predict-form");
const predictBtn = document.getElementById("predict-btn");
const statusLine = document.getElementById("status-line");
const loadScore = document.getElementById("load-score");
const confidenceScore = document.getElementById("confidence-score");
const summaryText = document.getElementById("summary-text");
const breakdownList = document.getElementById("breakdown-list");
const recommendations = document.getElementById("recommendations");
const healthPill = document.getElementById("health-pill");
const bandPill = document.getElementById("band-pill");
const scoreCard = document.getElementById("score-card");

function updateSliderLabels() {
  document.querySelectorAll("input[type='range']").forEach((input) => {
    const target = document.querySelector(`[data-value-for='${input.id}']`);
    if (target) target.textContent = input.value;
  });
}

function setPreset(name) {
  const preset = presets[name];
  if (!preset) return;
  document.getElementById("subject_id").value = preset.subject_id;
  document.getElementById("context").value = preset.context;
  Object.entries(preset.signals).forEach(([key, value]) => {
    const element = document.getElementById(key);
    if (element) element.value = value;
  });
  updateSliderLabels();
  statusLine.textContent = `Loaded preset: ${name}`;
}

function collectPayload() {
  return {
    subject_id: document.getElementById("subject_id").value,
    context: document.getElementById("context").value,
    signals: {
      eeg_focus_index: Number(document.getElementById("eeg_focus_index").value),
      theta_beta_ratio: Number(document.getElementById("theta_beta_ratio").value),
      blink_rate_per_min: Number(document.getElementById("blink_rate_per_min").value),
      hrv_rmssd: Number(document.getElementById("hrv_rmssd").value),
      typing_speed_wpm: Number(document.getElementById("typing_speed_wpm").value),
      typing_error_rate: Number(document.getElementById("typing_error_rate").value),
      mouse_hesitation_score: Number(document.getElementById("mouse_hesitation_score").value),
      task_switches_per_min: Number(document.getElementById("task_switches_per_min").value),
      session_duration_min: Number(document.getElementById("session_duration_min").value)
    }
  };
}

function renderResult(result) {
  loadScore.textContent = `${result.load_score}`;
  confidenceScore.textContent = `Confidence ${Math.round(result.confidence * 100)}%`;
  summaryText.textContent = result.summary;
  bandPill.textContent = result.load_band.toUpperCase();
  scoreCard.dataset.band = result.load_band;

  recommendations.innerHTML = "";
  result.recommendations.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    recommendations.appendChild(li);
  });

  breakdownList.innerHTML = "";
  result.modality_breakdown.forEach((item) => {
    const card = document.createElement("article");
    card.className = "breakdown-card";
    card.innerHTML = `
      <div class="breakdown-top">
        <strong>${item.modality}</strong>
        <span>${item.score}</span>
      </div>
      <div class="breakdown-bar"><span style="width:${item.score}%"></span></div>
      <p>${item.explanation}</p>
    `;
    breakdownList.appendChild(card);
  });
}

async function checkHealth() {
  try {
    const res = await fetch("/health");
    const data = await res.json();
    healthPill.textContent = data.status === "ok" ? "Healthy" : "Unknown";
  } catch (error) {
    healthPill.textContent = "Offline";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  predictBtn.disabled = true;
  predictBtn.textContent = "Scoring...";
  statusLine.textContent = "Running multimodal inference...";
  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectPayload())
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const result = await res.json();
    renderResult(result);
    statusLine.textContent = `Prediction ready for ${result.subject_id}.`;
  } catch (error) {
    statusLine.textContent = `Prediction failed: ${error.message}`;
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = "Run Prediction";
  }
});

document.querySelectorAll("input[type='range']").forEach((input) => {
  input.addEventListener("input", updateSliderLabels);
});

document.querySelectorAll("[data-preset]").forEach((button) => {
  button.addEventListener("click", () => setPreset(button.dataset.preset));
});

updateSliderLabels();
setPreset("baseline");
checkHealth();

