let plotCount = 0;

let xOptions = [];
let yOptions = [];


/* ==========================================================
   Plotly Loader
========================================================== */

const PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.35.2.min.js";

function ensurePlotlyLoaded() {

    if (window.Plotly) {

        return Promise.resolve();

    }

    return new Promise((resolve, reject) => {

        const existingScript = document.querySelector(
            `script[src="${PLOTLY_CDN}"]`
        );

        if (existingScript) {

            existingScript.onload = () => resolve();

            existingScript.onerror = () => reject(
                new Error("Failed to load Plotly.")
            );

            return;

        }

        const script = document.createElement("script");

        script.src = PLOTLY_CDN;

        script.onload = () => resolve();

        script.onerror = () => reject(
            new Error("Failed to load Plotly.")
        );

        document.head.appendChild(script);

    });

}


/* ==========================================================
   Initialize
========================================================== */

async function initializePlots() {

    const options = await getPlotOptions();

    xOptions = options.x || [];

    yOptions = options.y || [];

}


/* ==========================================================
   Add Plot
========================================================== */

function addPlot() {

    plotCount++;

    const card = document.createElement("div");

    card.className = "plot-card";

    card.innerHTML = `

        <h3>
            Plot ${plotCount}
        </h3>

        <div class="plot-grid">

            <div>
                <label>
                    X Axis
                </label>

                <select class="x-axis">
                </select>
            </div>

            <div>
                <label>
                    Y Axis
                </label>

                <select class="y-axis">
                </select>
            </div>

            <div>
                <label>
                    Bins
                </label>

                <input
                    class="bins"
                    type="number"
                    value="20"
                    min="2"
                >
            </div>

        </div>

        <div class="button-group">

            <button class="generate-btn">
                Generate
            </button>

            <button class="delete-btn">
                Delete
            </button>

        </div>

        <div class="plot-output">
        </div>

    `;

    document
        .getElementById("plots")
        .appendChild(card);

    populateXAxis(card);

    populateYAxis(card);

    bindEvents(card);

}


/* ==========================================================
   Populate X Axis
========================================================== */

function populateXAxis(card) {

    const select = card.querySelector(".x-axis");

    select.innerHTML = "";

    xOptions.forEach(option => {

        const element = document.createElement("option");

        element.value = option;

        element.textContent = option;

        select.appendChild(element);

    });

}


/* ==========================================================
   Populate Y Axis
========================================================== */

function populateYAxis(card) {

    const select = card.querySelector(".y-axis");

    select.innerHTML = "";

    yOptions.forEach(option => {

        const element = document.createElement("option");

        element.value = option;

        element.textContent = option;

        select.appendChild(element);

    });

}


/* ==========================================================
   Execute Scripts Inside Plotly HTML
========================================================== */

async function renderPlotHtml(output, html) {

    await ensurePlotlyLoaded();

    output.innerHTML = "";

    output.style.minHeight = "500px";

    output.style.width = "100%";

    output.innerHTML = html;

    const scripts = Array.from(
        output.querySelectorAll("script")
    );

    for (const oldScript of scripts) {

        const newScript = document.createElement("script");

        if (oldScript.src) {

            await loadScript(oldScript.src);

        }

        else {

            newScript.text = oldScript.textContent;

            document.body.appendChild(newScript);

            document.body.removeChild(newScript);

        }

        oldScript.remove();

    }

    window.dispatchEvent(
        new Event("resize")
    );

}


function loadScript(src) {

    return new Promise((resolve, reject) => {

        if (
            Array.from(document.scripts)
                .some(script => script.src === src)
        ) {

            resolve();

            return;

        }

        const script = document.createElement("script");

        script.src = src;

        script.onload = () => resolve();

        script.onerror = () => reject(
            new Error(`Failed to load script: ${src}`)
        );

        document.head.appendChild(script);

    });

}


/* ==========================================================
   Events
========================================================== */

function bindEvents(card) {

    const generate = card.querySelector(".generate-btn");

    const remove = card.querySelector(".delete-btn");

    const output = card.querySelector(".plot-output");

    remove.onclick = () => {

        card.remove();

    };

    generate.onclick = async () => {

        const x = card
            .querySelector(".x-axis")
            .value;

        const y = card
            .querySelector(".y-axis")
            .value;

        const bins = Number(
            card
                .querySelector(".bins")
                .value
        );

        showLoading("Generating Plot...");

        try {

            const html = await generatePlot(
                x,
                y,
                bins
            );

            await renderPlotHtml(
                output,
                html
            );

        }

        catch (err) {

            console.error(err);

            output.innerHTML = `

                <p style="color:red;">
                    Failed to generate plot.
                </p>

            `;

        }

        finally {

            hideLoading();

        }

    };

}