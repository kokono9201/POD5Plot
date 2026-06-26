let pod5 = null;


/* ==========================================================
   Loading
========================================================== */

function showLoading(message = "Loading...") {

    const overlay = document.getElementById("loading-overlay");

    overlay.style.display = "flex";

    document
        .getElementById("loading-title")
        .innerText = message;

}


function hideLoading() {

    document
        .getElementById("loading-overlay")
        .style.display = "none";

}


/* ==========================================================
   Dashboard
========================================================== */

async function initializeDashboard() {

    await loadSummary();

    await loadRunInfo();

    await initializePlots();

}


/* ==========================================================
   Select POD5
========================================================== */

document
    .getElementById("select-btn")
    .addEventListener("click", async () => {

        pod5 = await selectPod5();

        if (!pod5)
            return;

        document
            .getElementById("selected-file")
            .innerText = pod5.filename;

    });


/* ==========================================================
   Analyze
========================================================== */

document
    .getElementById("analyze-btn")
    .addEventListener("click", async () => {

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

    });


/* ==========================================================
   Copy
========================================================== */

document
    .getElementById("copy-summary")
    .addEventListener("click", copySummary);


document
    .getElementById("copy-run-info")
    .addEventListener("click", copyRunInfo);


/* ==========================================================
   Export
========================================================== */

async function buildDashboardExportHtml() {

    const dashboard = document
        .getElementById("dashboard-page")
        .cloneNode(true);

    dashboard.style.display = "block";

    dashboard
        .querySelectorAll("button")
        .forEach(button => {

            button.remove();

        });

    dashboard
        .querySelectorAll(".button-group")
        .forEach(group => {

            if (group.children.length === 0) {

                group.remove();

            }

        });

    let css = "";

    try {

        const response = await fetch(
            "/static/css/style.css"
        );

        css = await response.text();

    }

    catch (err) {

        console.error(
            "Failed to load CSS for export:",
            err
        );

    }

    const title = pod5
        ? pod5.filename
        : "POD5Plot Dashboard";

    return `

<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>${title}</title>

    <style>

        ${css}

        body {
            background: #f5f6fa;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 40px;
        }

        .plot-output {
            min-height: 500px;
            width: 100%;
        }

        .plotly-graph-div {
            min-height: 500px;
        }

    </style>

</head>

<body>

    <div class="container">

        ${dashboard.outerHTML}

    </div>

</body>

</html>

`;

}


document
    .getElementById("export-dashboard")
    .addEventListener("click", async () => {

        if (!pod5)
            return;

        showLoading("Exporting Dashboard...");

        try {

            const html = await buildDashboardExportHtml();

            const outputPath = await exportDashboard(
                html,
                pod5.filename
            );

            hideLoading();

            alert(
                `Dashboard exported:\n${outputPath}`
            );

        }

        catch (err) {

            hideLoading();

            console.error(err);

            alert(
                "Export failed."
            );

        }

    });


/* ==========================================================
   Plot
========================================================== */

document
    .getElementById("add-plot")
    .addEventListener("click", () => {

        addPlot();

    });