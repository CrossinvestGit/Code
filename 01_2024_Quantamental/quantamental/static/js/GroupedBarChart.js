class GroupedBarChart {

    constructor(_parentElement, _data, _xdata, _ydata, _cdata, _legend = { noCol: 1, widthCol: 65 }) {
        this.parentElement = _parentElement;
        this.data = _data;
        this.xdata = _xdata;
        this.ydata = _ydata;
        this.cdata = _cdata;
        this.legend = _legend;
        this.initVis();
    }

    initVis() {
        const vis = this;

        vis.MARGIN = { TOP: 50, RIGHT: 5, BOTTOM: 50, LEFT: 80 };
        vis.WIDTH = 829 - vis.MARGIN.LEFT - vis.MARGIN.RIGHT;
        vis.HEIGHT = 500 - vis.MARGIN.TOP - vis.MARGIN.BOTTOM;

        vis.svg = d3.select(vis.parentElement).append("svg")
            .attr("viewBox", [0, 0, vis.WIDTH + vis.MARGIN.LEFT + vis.MARGIN.RIGHT, vis.HEIGHT + vis.MARGIN.TOP + vis.MARGIN.BOTTOM])
            .attr("width", vis.WIDTH + vis.MARGIN.LEFT + vis.MARGIN.RIGHT)
            .attr("height", vis.HEIGHT + vis.MARGIN.TOP + vis.MARGIN.BOTTOM)
            .attr("style", "max-width: 100%; height: auto; height: intrinsic; font: 10px sans-serif;")
            .style("-webkit-tap-highlight-color", "transparent")
            .style("overflow", "visible");

        vis.canvas = vis.svg.append("g")
            .attr("class", "canvas") // Set the class attribute
            .attr("transform", `translate(${vis.MARGIN.LEFT}, ${vis.MARGIN.TOP})`);

        vis.xLabel = vis.canvas.append("text")
            .attr("class", "x axis-label")
            .attr("x", vis.WIDTH / 2)
            .attr("y", vis.HEIGHT + 60)
            .attr("font-size", "20px")
            .attr("text-anchor", "middle")

        vis.yLabel = vis.canvas.append("text")
            .attr("class", "y axis-label")
            .attr("x", - (vis.HEIGHT / 2))
            .attr("y", -60)
            .attr("font-size", "20px")
            .attr("text-anchor", "middle")
            .attr("transform", "rotate(-90)");

        vis.fx = d3.scaleBand()
            .domain(vis.data.map(d => d[vis.xdata]))
            .rangeRound([0, vis.WIDTH])
            .paddingInner(0.1);

        vis.x = d3.scaleBand()
            .rangeRound([0, vis.fx.bandwidth()])
            .padding(0.05);

        vis.y = d3.scaleLinear()
            .rangeRound([vis.HEIGHT, 0])
            .nice();

        vis.fxAxisGroup = vis.canvas.append("g")
            .attr("class", "x axis");

        vis.yAxisGroup = vis.canvas.append("g")
            .attr("class", "y axis")
            .call(d3.axisLeft(vis.y).ticks(null, "s"));

        vis.maxDotsPerColumn = vis.legend["noCol"]; // Maximum number of dots per column in the legend
        vis.columnWidth = vis.legend["widthCol"]; // Width of each column in the legend

        vis.legendOffsetY = -vis.maxDotsPerColumn * (vis.maxDotsPerColumn + 1) * 5; // Offset for the legend in the y-direction
        vis.fontWeight = "bold"; // Font weight for the legend text
        vis.dotRadius = 5; // Radius of the legend dots
        vis.dotSpacing = 20; // Spacing between legend dots
        vis.textOffsetX = 10; // Offset for the legend text in the x-direction

        vis.manageData();
    }

    manageData() {
        const vis = this;
        vis.updateVis();
    }

    updateVis() {
        const vis = this;
        const t = d3.transition().duration(750);

        vis.color = d3.scaleOrdinal()
            .range(d3.schemeCategory10);

        // Update scales
        vis.y.domain([d3.min(vis.data, d => d[vis.ydata]), d3.max(vis.data, d => d[vis.ydata])]);
        vis.x.domain(vis.data.map(d => d[vis.cdata]));
        vis.fx.domain(vis.data.map(d => d[vis.xdata]));

        // Draw rectangles
        const rects = vis.canvas.selectAll("rect")
            .data(vis.data, d => d[vis.xdata] + d[vis.cdata]);

        rects.exit()
            .transition(t)
            .attr("height", 0)
            .attr("y", vis.y(0))
            .remove();

        vis.canvas.selectAll(".legend-circle").remove();
        vis.canvas.selectAll(".legend-text").remove();

        vis.dataLabel = [...new Set(vis.data.map(item => item[vis.cdata]))];
        vis.legendOffsetX = (vis.WIDTH - (vis.dataLabel.length * vis.columnWidth)) / 2; // Offset for the legend in the x-direction

        let i = 0; // Counter variable
        for (const thisDataLabel of vis.dataLabel) {
            const column = Math.floor(i / vis.maxDotsPerColumn); // Calculate the column index
            const dotX = vis.legendOffsetX + column * vis.columnWidth; // Calculate the x-coordinate of the legend dot
            const dotY = vis.legendOffsetY + (i % vis.maxDotsPerColumn) * vis.dotSpacing; // Calculate the y-coordinate of the legend dot

            const legendCircle = vis.canvas.append("circle") // Append a circle element for the legend dot
                .attr("class", "legend-circle")
                .attr("cx", dotX) // Set the cx attribute
                .attr("cy", dotY) // Set the cy attribute
                .attr("r", vis.dotRadius) // Set the r attribute
                .style('fill', vis.color(thisDataLabel)); // Set the fill color

            const legendText = vis.canvas.append("text") // Append a text element for the legend text
                .attr("class", "legend-text")
                .attr("x", dotX + vis.textOffsetX) // Set the x attribute
                .attr("y", dotY + 1) // Set the y attribute
                .text(thisDataLabel) // Set the text content
                .attr("text-anchor", "left") // Set the text-anchor attribute
                .style("alignment-baseline", "middle") // Set the alignment-baseline style
                .style("font-weight", vis.fontWeight); // Set the font-weight style

            i++; // Increment the counter
        }

        rects.enter().append("rect")
            .merge(rects)
            .transition(t)
            .attr("x", d => vis.fx(d[vis.xdata]) + vis.x(d[vis.cdata]))
            .attr("y", d => d[vis.ydata] >= 0 ? vis.y(d[vis.ydata]) : vis.y(0))
            .attr("width", vis.x.bandwidth())
            .attr("height", d => Math.abs(vis.y(0) - vis.y(d[vis.ydata])))
            .attr("fill", d => vis.color(d[vis.cdata]));

        // Draw y-axis
        vis.yAxisCall = d3.axisLeft(vis.y);
        vis.yAxisGroup.transition(t).call(vis.yAxisCall);

        // Remove old x-axis group with transition
        vis.fxAxisGroup.transition(t)
            .style("opacity", 0)
            .remove();

        // Create a new group for x-axis labels
        vis.fxAxisGroup = vis.canvas.append("g")
            .attr("class", "x axis")
            .style("opacity", 0); // Start with opacity 0

        // Draw x-axis with transition
        vis.fxAxisCall = d3.axisBottom(vis.fx);
        vis.fxAxisGroup
            .attr("transform", `translate(0, ${vis.y(0)})`)
            .transition(t)
            .style("opacity", 1) // Transition to opacity 1
            .call(vis.fxAxisCall)
            .selectAll("text")
            .attr("y", "10")
            .attr("x", "-5")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-40)");
    }
}