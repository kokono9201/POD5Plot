async function selectPod5() {

    return await window.pywebview.api.select_pod5();

}


async function analyze() {

    return await window.pywebview.api.analyze();

}


async function getSummary() {

    return await window.pywebview.api.get_summary();

}


async function getRunInfo() {

    return await window.pywebview.api.get_run_info();

}


async function getColumns() {

    return await window.pywebview.api.get_columns();

}


async function exportPdf() {

    return await window.pywebview.api.export_pdf();

}