async function selectPod5() {

    const result = await window.pywebview.api.select_pod5();

    if (!result) {
        return;
    }

    document.getElementById("selected-file").innerText =
        result.filename;
}

document
    .getElementById("select-btn")
    .addEventListener("click", selectPod5);