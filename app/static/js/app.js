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
   Export Dashboard
========================================================== */

async function buildDashboardExportHtml() {

    const sourceDashboard = document
        .getElementById("dashboard-page");

    const dashboard = sourceDashboard.cloneNode(true);

    dashboard.style.display = "block";

    await replacePlotsWithImages(
        sourceDashboard,
        dashboard
    );

    cleanDashboardForExport(
        dashboard
    );

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

    <title>${escapeHtml(title)}</title>

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

        .plot-card {
            page-break-inside: avoid;
            break-inside: avoid;
        }

        .plot-output {
            width: 100%;
            min-height: auto;
            overflow: visible;
        }

        .export-plot-image {
            display: block;
            width: 100%;
            height: auto;
            margin-top: 20px;
        }

        .dashboard-header {
            margin-bottom: 40px;
        }

        @media print {

            body {
                background: white;
            }

            .container {
                padding: 20px;
            }

            .plot-card {
                page-break-inside: avoid;
                break-inside: avoid;
            }

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


async function replacePlotsWithImages(
    sourceDashboard,
    clonedDashboard
) {

    const sourceOutputs = Array.from(
        sourceDashboard.querySelectorAll(".plot-output")
    );

    const clonedOutputs = Array.from(
        clonedDashboard.querySelectorAll(".plot-output")
    );

    for (let index = 0; index < sourceOutputs.length; index++) {

        const sourceOutput = sourceOutputs[index];

        const clonedOutput = clonedOutputs[index];

        if (!clonedOutput)
            continue;

        const plotDiv = sourceOutput.querySelector(
            ".js-plotly-plot, .plotly-graph-div"
        );

        if (!plotDiv)
            continue;

        if (!window.Plotly || !Plotly.toImage)
            continue;

        try {

            const rect = plotDiv.getBoundingClientRect();

            const width = Math.max(
                Math.round(rect.width),
                900
            );

            const height = Math.max(
                Math.round(rect.height),
                500
            );

            const image = await Plotly.toImage(
                plotDiv,
                {
                    format: "png",
                    width: width,
                    height: height,
                    scale: 2
                }
            );

            clonedOutput.innerHTML = `

                <img
                    class="export-plot-image"
                    src="${image}"
                    alt="POD5Plot chart"
                >

            `;

        }

        catch (err) {

            console.error(
                "Failed to convert plot to image:",
                err
            );

            clonedOutput.innerHTML = sourceOutput.innerHTML;

        }

    }

}


function cleanDashboardForExport(dashboard) {

    dashboard
        .querySelectorAll("button")
        .forEach(button => {

            button.remove();

        });

    dashboard
        .querySelectorAll(".plot-grid")
        .forEach(grid => {

            grid.remove();

        });

    dashboard
        .querySelectorAll(".button-group")
        .forEach(group => {

            if (group.children.length === 0) {

                group.remove();

            }

        });

}


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

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