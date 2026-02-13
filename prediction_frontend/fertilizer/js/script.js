const predictBtn = document.getElementById("predictBtn");
const resetBtn = document.getElementById("resetBtn");
const resultDiv = document.getElementById("result");

predictBtn.addEventListener("click", function () {
  const crop = document.getElementById("crop").value;
  const n = document.getElementById("nitrogen").value;
  const p = document.getElementById("phosphorus").value;
  const k = document.getElementById("potassium").value;

  const data = {
    crop: crop,
    soil: "Loamy",
    N: parseFloat(n),
    P: parseFloat(p),
    K: parseFloat(k),
    ph: 7,
    rainfall: 100,
    temperature: 25
  };

  fetch("http://127.0.0.1:5000/predict_fertilizer", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(result => {
    if (result.fertilizer) {
      document.getElementById("result").innerHTML = `
        ✅ <strong>Recommended Fertilizer:</strong> ${result.fertilizer}
      `;
    } else {
      document.getElementById("result").innerText = "Error: " + (result.error || "Unknown error");
    }
  })
  .catch(err => {
    console.error(err);
    document.getElementById("result").innerText = "Backend connection failed!";
  });
});
