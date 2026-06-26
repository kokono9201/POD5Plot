/* ==========================================================
   File
========================================================== */

async function selectPod5() {

    return await window.pywebview.api.select_pod5();

}


/* ==========================================================
   Analyze
========================================================== */

async function analyze() {

    return await window.pywebview.api.analyze();

}


/* ==========================================================
   Summary
========================================================== */

async function getSummary() {

    return await window.pywebview.api.get_summary();

}


/* ==========================================================
   Run Information
========================================================== */

async function getRunInfo() {

    return await window.pywebview.api.get_run_info();

}


/* ==========================================================
   Plot Options
========================================================== */

async function getPlotOptions() {

    return await window.pywebview.api.get_plot_options();

}


/* ==========================================================
   Plot
========================================================== */

async function generatePlot(
    x,
    y,
    bins = 20
) {

    return await window.pywebview.api.generate_plot(
        x,
        y,
        bins
    );

}

/* ==========================================================
   Export
========================================================== */

async function exportDashboard(
    html,
    filename
) {

    return await window.pywebview.api.export_dashboard(
        html,
        filename
    );

}