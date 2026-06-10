//////////////////////////////
// 🔹 ANALYZE FUNCTION
//////////////////////////////
function analyzeWebsite() {
    const url = document.getElementById("urlInput").value.trim();
    const loader = document.getElementById("loader");
    const errorMsg = document.getElementById("errorMsg");

    // Reset UI
    errorMsg.innerText = "";

    if (url === "") {
        errorMsg.innerText = "⚠️ Please enter a website URL";
        return;
    }

    // Show loader
    if (loader) loader.classList.remove("hidden");

    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("resultData", JSON.stringify(data));
        window.location.href = "result.html";
    })
    .catch(error => {
        errorMsg.innerText = "❌ Backend not running. Start server first.";
        console.error(error);
    })
    .finally(() => {
        if (loader) loader.classList.add("hidden");
    });
}

//////////////////////////////
// 🔐 SAFE SEARCH FUNCTION (NEW)
//////////////////////////////
function openGoogleSearch() {
    const body = document.body;

    // Flip animation
    body.classList.add("flip");

    setTimeout(() => {
        let url = "";

        // index page se URL lena
        const input = document.getElementById("urlInput");
        if (input) {
            url = input.value;
        }

        // result page ke liye (localStorage se)
        if (!url) {
            const data = JSON.parse(localStorage.getItem("resultData"));
            if (data && data.url) {
                url = data.url;
            }
        }

        // Google search open
        window.open(`https://www.google.com/search?q=${url}`, "_blank");

        body.classList.remove("flip");
    }, 600);
}

//////////////////////////////
// 🔹 RESULT PAGE LOGIC
//////////////////////////////
window.onload = function () {
    const data = JSON.parse(localStorage.getItem("resultData"));
    if (!data) return;

    // Elements
    const statusText = document.getElementById("statusText");
    const trustValue = document.getElementById("trustValue");
    const trustFill = document.getElementById("trustFill");
    const reviewText = document.getElementById("reviewText");
    const recommendText = document.getElementById("recommendText");
    const aiText = document.getElementById("aiText");
    const safeList = document.getElementById("safeList");

    //////////////////////////////
    // 🔥 STATUS + COLOR LOGIC
    //////////////////////////////
    statusText.innerText = data.status || "Unknown";

    if (data.status === "Genuine") {
        statusText.style.color = "#00ff88";
    } else if (data.status === "Suspicious") {
        statusText.style.color = "#ffcc00";
    } else {
        statusText.style.color = "#ff4d4d";
    }

    //////////////////////////////
    // 📊 TRUST SCORE ANIMATION
    //////////////////////////////
    let score = data.trust_score || 0;
    trustValue.innerText = score + "% Trusted";

    let width = 0;
    const interval = setInterval(() => {
        if (width >= score) {
            clearInterval(interval);
        } else {
            width++;
            trustFill.style.width = width + "%";
        }
    }, 10);

    //////////////////////////////
    // 🤖 AI EXPLANATION
    //////////////////////////////
    aiText.innerText = data.ai_explanation || "No AI insights available.";

    //////////////////////////////
    // 💬 REVIEW ANALYSIS
    //////////////////////////////
    reviewText.innerText = data.review || "No review data available.";

    //////////////////////////////
    // ✅ RECOMMENDATION
    //////////////////////////////
    recommendText.innerText = data.recommendation || "Stay cautious.";

    //////////////////////////////
    // 🔗 SAFE ALTERNATIVES
    //////////////////////////////
    safeList.innerHTML = "";

    if (data.safe_sites && data.safe_sites.length > 0) {
        data.safe_sites.forEach(site => {
            const li = document.createElement("li");
            li.innerHTML = `<a href="https://${site}" target="_blank">${site}</a>`;
            safeList.appendChild(li);
        });
    } else {
        safeList.innerHTML = "<li>No alternatives found</li>";
    }
};
const btn = document.getElementById("theme-toggle");

btn.addEventListener("click", () => {

    document.body.classList.toggle("dark-mode");

    if(document.body.classList.contains("dark-mode")){
        btn.innerHTML = "☀️ Day Mode";
    } else {
        btn.innerHTML = "🌙 Dark Mode";
    }

});