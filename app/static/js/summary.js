async function loadSummary() {

    const summary = await getSummary();

    const container = document.getElementById("summary");

    container.innerHTML = "";

    for (const key in summary) {

        const card = document.createElement("div");

        card.className = "summary-card";

        let value = summary[key];

        if (typeof value === "number") {

            value = Number(value).toFixed(2);

        }

        card.innerHTML = `

            <h3>${key}</h3>

            <p>${value}</p>

        `;

        container.appendChild(card);

    }

}



async function loadRunInfo() {

    const runInfo = await getRunInfo();

    const tbody = document.querySelector(
        "#run-info-table tbody"
    );

    tbody.innerHTML = "";

    for (const key in runInfo) {

        const row = document.createElement("tr");

        row.innerHTML = `

            <td>${key}</td>

            <td>${runInfo[key]}</td>

        `;

        tbody.appendChild(row);

    }

}



async function copySummary() {

    const summary = await getSummary();

    let text = "";

    for (const key in summary) {

        text += `${key}: ${summary[key]}\n`;

    }

    navigator.clipboard.writeText(text);

}



async function copyRunInfo() {

    const info = await getRunInfo();

    let text = "";

    for (const key in info) {

        text += `${key}: ${info[key]}\n`;

    }

    navigator.clipboard.writeText(text);

}