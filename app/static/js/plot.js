let plotId = 0;

function addPlot(){

    plotId++;

    const html = `

<div class="plot-card">

<h3>

Plot ${plotId}

</h3>

<p>

Plot Builder

</p>

</div>

`;

    document

        .getElementById("plots")

        .insertAdjacentHTML(

            "beforeend",

            html

        );

}