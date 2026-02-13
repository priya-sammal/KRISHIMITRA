const langBox = document.querySelector('.change-language');
const en = langBox.querySelector('.english');
const hi = langBox.querySelector('.hindi');

langBox.addEventListener('click', () => {
    
    // If English is visible → switch to Hindi
    if (!en.classList.contains('hidden')) {
        en.classList.add('hidden');
        hi.classList.remove('hidden');
    }

    // Else English was hidden → show English again
    else {
        en.classList.remove('hidden');
        hi.classList.add('hidden');
    }
});



//sharing 
const siteURL = window.location.href; 

document.querySelector(".whatsapp").addEventListener("click", () => {
    window.open(`https://wa.me/?text=${encodeURIComponent(siteURL)}`, "_blank");
});

document.querySelector(".facebook").addEventListener("click", () => {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(siteURL)}`, "_blank");
});

document.querySelector(".instagram").addEventListener("click", () => {
    navigator.clipboard.writeText(siteURL);
    alert("Link copied! Share it on Instagram.");
});
// ================================
// CROP PREDICTION
// ================================
function predictCrop() {
  const data = {
    N: document.getElementById("N").value,
    P: document.getElementById("P").value,
    K: document.getElementById("K").value,
    temperature: document.getElementById("temperature").value,
    humidity: document.getElementById("humidity").value,
    ph: document.getElementById("ph").value,
    rainfall: document.getElementById("rainfall").value
  };

  fetch("http://127.0.0.1:5000/predict_crop", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(result => {
    console.log(result);
    document.getElementById("cropResult").innerText =
      "Recommended Crop: " + result.crop;
  })
  .catch(err => {
    console.error("Error:", err);
    alert("Error connecting to backend");
  });
}


// ================================
// FERTILIZER PREDICTION
// ================================
function predictFertilizer() {
  const data = {
    N: document.getElementById("fN").value,
    P: document.getElementById("fP").value,
    K: document.getElementById("fK").value,
    temperature: document.getElementById("fTemperature").value,
    rainfall: document.getElementById("fRainfall").value,
    ph: document.getElementById("fPh").value,
    crop: document.getElementById("crop").value,
    soil: document.getElementById("soil").value
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
    console.log(result);
    document.getElementById("fertilizerResult").innerText =
      "Recommended Fertilizer: " + result.fertilizer;
  })
  .catch(err => {
    console.error("Error:", err);
    alert("Error connecting to backend");
  });
}
