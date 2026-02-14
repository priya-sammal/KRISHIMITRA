const chartCanvas = document.getElementById("resultChart");
let resultChart = null; // to destroy old chart before drawing new one

const predictBtn = document.getElementById("predictBtn");
const resetBtn = document.getElementById("resetBtn");
const resultDiv = document.getElementById("result");
const loader = document.getElementById("loader");
const confidenceBar = document.getElementById("confidenceBar");
const confidenceText = document.getElementById("confidenceText");

predictBtn.addEventListener("click", function () {
  const crop = document.getElementById("crop").value;
  const soil = document.getElementById("soil").value;
  const n = document.getElementById("nitrogen").value;
  const p = document.getElementById("phosphorus").value;
  const k = document.getElementById("potassium").value;
  const ph = document.getElementById("ph").value;
  const rainfall = document.getElementById("rainfall").value;
  const temperature = document.getElementById("temperature").value;

  const data = {
    crop: crop.toLowerCase().trim(),
    soil: soil.toLowerCase().trim(),
    N: parseFloat(n),
    P: parseFloat(p),
    K: parseFloat(k),
    ph: parseFloat(ph),
    rainfall: parseFloat(rainfall),
    temperature: parseFloat(temperature),
  };

  // UI: show loader
  loader.classList.remove("hidden");
  resultDiv.classList.remove("success");
  resultDiv.innerHTML = "Predicting...";
  confidenceBar.style.width = "0%";
  confidenceText.innerText = "--%";

  fetch("http://127.0.0.1:5000/predict_fertilizer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((result) => {
      loader.classList.add("hidden");

      if (result.fertilizer) {
        resultDiv.classList.add("success");

        let html = `<h3>✅ Recommended Fertilizer</h3>
              <p><strong>${result.fertilizer}</strong></p>`;

        // Top 3 list
        if (result.top3) {
          html += "<h4>Top 3 Suggestions</h4><ul>";
          result.top3.forEach((item) => {
            html += `<li>${item.fertilizer} — ${item.confidence}%</li>`;
          });
          html += "</ul>";
        }

        resultDiv.innerHTML = html;

        // Real confidence
        const confidence = result.confidence;
        confidenceBar.style.width = confidence + "%";
        confidenceText.innerText = confidence + "% confidence";

        // Animate progress bar
        confidenceBar.classList.add("animate-bar");

        // =========================
        // 📊 CHART.JS PART (TOP 3)
        // =========================
        if (result.top3 && chartCanvas) {
          const labels = result.top3.map((item) => item.fertilizer);
          const dataValues = result.top3.map((item) => item.confidence);

          // Destroy old chart if exists
          // 🔥 Destroy existing chart on this canvas (if any)
        const existingChart = Chart.getChart(chartCanvas);
        if (existingChart) {
            existingChart.destroy();
        }


          const ctx = chartCanvas.getContext("2d");
          resultChart = new Chart(ctx, {
            type: "bar",
            data: {
              labels: labels,
              datasets: [
                {
                  label: "Confidence (%)",
                  data: dataValues,
                  borderWidth: 1,
                },
              ],
            },
            options: {
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true,
                  max: 100,
                },
              },
              plugins: {
                legend: {
                  display: false,
                },
                title: {
                  display: true,
                  text: "Top 3 Fertilizer Predictions",
                },
              },
            },
          });
        }
      } else {
        resultDiv.innerText = "Error: " + (result.error || "Unknown error");
      }
    })
    .catch((err) => {
      console.error(err);
      loader.classList.add("hidden");
      resultDiv.innerText = "Backend connection failed!";
    });
});

resetBtn.addEventListener("click", function () {
  resultDiv.innerHTML = "Enter values and click Recommend Fertilizer.";
  resultDiv.classList.remove("success");
  confidenceBar.style.width = "0%";
  confidenceText.innerText = "--%";

  if (resultChart) {
    resultChart.destroy();
    resultChart = null;
  }
});

