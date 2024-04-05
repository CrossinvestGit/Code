class GroupedBarChart {

    constructor(_parentElement, _data) {
        this.parentElement = _parentElement;
        this.data = _data;
        this.initVis();
    }

    initVis() {
        const vis = this;
        const data = vis.data;

        // Define margins and dimensions for the SVG container
        vis.MARGIN = { TOP: 50, RIGHT: 5, BOTTOM: 50, LEFT: 80 };
        vis.WIDTH = 829 - vis.MARGIN.LEFT - vis.MARGIN.RIGHT;
        vis.HEIGHT = 500 - vis.MARGIN.TOP - vis.MARGIN.BOTTOM;

        // Create the SVG container
        vis.svg = d3.select(vis.parentElement).append("svg")
            .attr("viewBox", [0, 0, vis.WIDTH + vis.MARGIN.LEFT + vis.MARGIN.RIGHT, vis.HEIGHT + vis.MARGIN.TOP + vis.MARGIN.BOTTOM])
            .attr("width", vis.WIDTH + vis.MARGIN.LEFT + vis.MARGIN.RIGHT)
            .attr("height", vis.HEIGHT + vis.MARGIN.TOP + vis.MARGIN.BOTTOM)
            .attr("style", "max-width: 100%; height: auto; height: intrinsic; font: 10px sans-serif;")
            .style("-webkit-tap-highlight-color", "transparent")
            .style("overflow", "visible");

        // Create a group element within the SVG
        vis.g = vis.svg.append("g")
            .attr("transform", `translate(${vis.MARGIN.LEFT}, ${vis.MARGIN.TOP})`);

        // Define x-axis scale
        vis.fx = d3.scaleBand()
            .domain(data.map(d => d.Year))
            .rangeRound([0, vis.WIDTH])
            .paddingInner(0.1);

        // Extract unique stocks from the data
        const stocks = Array.from(new Set(data.map(d => d.Stock)));

        // Define x-axis scale for grouped bars
        vis.x = d3.scaleBand()
            .domain(stocks)
            .rangeRound([0, vis.fx.bandwidth()])
            .padding(0.05);

        // Define color scale
        const color = d3.scaleOrdinal()
            .domain(stocks)
            .range(d3.schemeCategory10);

        // Define y-axis scale
        vis.y = d3.scaleLinear()
            .domain([d3.min(data, d => d.Percentage), d3.max(data, d => d.Percentage)])
            .rangeRound([vis.HEIGHT, 0])
            .nice();

        // Render the grouped bars
        vis.g.selectAll()
            .data(d3.group(data, d => d.Year))
            .enter().append("g")
            .attr("transform", d => `translate(${vis.fx(d[0])}, 0)`)
            .selectAll("rect")
            .data(d => d[1])
            .enter().append("rect")
            .attr("x", d => vis.x(d.Stock))
            .attr("y", d => {
                if (d.Percentage >= 0) {
                    return vis.y(d.Percentage);
                } else {
                    return vis.y(0);
                }
            })
            .attr("width", vis.x.bandwidth())
            .attr("height", d => Math.abs(vis.y(0) - vis.y(d.Percentage)))
            .attr("fill", d => color(d.Stock));

        // Render x-axis
        vis.g.append("g")
            .attr("class", "x axis")
            .attr("transform", `translate(0, ${vis.y(0)})`)  // Fixed x-axis at 0
            .call(d3.axisBottom(vis.fx).tickSizeOuter(0));

        // Render y-axis
        vis.g.append("g")
            .attr("class", "y axis")
            .call(d3.axisLeft(vis.y).ticks(null, "s"));
    }
}
