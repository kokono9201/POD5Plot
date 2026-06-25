let pod5 = null;


/* ==========================================================
   Loading
========================================================== */

function showLoading(message = "Analyzing POD5...") {

    const overlay = document.getElementById("loading-overlay");

    overlay.style.display = "flex";

    overlay.querySelector("h2").innerText = message;

}


function hideLoading() {

    document.getElementById("loading-overlay").style.display = "none";

}


/* ==========================================================
   Dashboard
========================================================== */

async function initializeDashboard() {

    await loadSummary();

    await loadRunInfo();

}


/* ==========================================================
   Select POD5
========================================================== */

document
    .getElementById("select-btn")
    .onclick = async () => {

        pod5 = await selectPod5();

        if (!pod5)
            return;

        document
            .getElementById("selected-file")
            .innerText = pod5.filename;

    };


/* ==========================================================
   Analyze
========================================================== */

document
    .getElementById("analyze-btn")
    .onclick = async () => {

        if (!pod5)
            return;

        showLoading("Analyzing POD5...");

        const ok = await analyze();

        hideLoading();

        if (!ok)
            return;

        document
            .getElementById("current-file")
            .innerText = pod5.filename;

        document
            .getElementById("home-page")
            .style.display = "none";

        document
            .getElementById("dashboard-page")
            .style.display = "block";

        await initializeDashboard();

    };


/* ==========================================================
   Copy
========================================================== */

document
    .getElementById("copy-summary")
    .onclick = copySummary;


document
    .getElementById("copy-run-info")
    .onclick = copyRunInfo;


/* ==========================================================
   Export Dashboard
========================================================== */

document
    .getElementById("export-pdf")
    .onclick = () => {

        alert("Export Dashboard is not implemented yet.");

    };


/* ==========================================================
   Plot
========================================================== */

document
    .getElementById("add-plot")
    .onclick = addPlot;