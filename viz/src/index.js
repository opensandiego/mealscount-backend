import _ from "lodash";
import * as d3 from "d3";
import data from "./data/data.json";

function appendFullDataTable() {
  d3.select("body")
    .append("div")
    .classed("mui-divider", true);
  var tableContainer = d3
    .select("body")
    .append("div")
    .classed("mui-container", true);

  var table = tableContainer.append("table").classed("mui-table--bordered", true);
  var thead = table.append("thead");
  var tbody = table.append("tbody");

  thead.append("th").text("District");
  thead.append("th").text("Code");
  thead.append("th").text("Total enrolled");
  thead.append("th").text("# Schools");
  thead.append("th").text("ISP Best");

  var tr = tbody
    .selectAll("tr")
    .data(data)
    .enter()
    .append("tr");

  var td = tr
    .selectAll("td")
    .data(function(d) {
      return [d.district, d.code, d["total enrolled"], d["# schools"], d["ISP Best"]];
    })
    .enter()
    .append("td")
    .text(function(d) {
      return d;
    });
}

function main() {
  // TODO create Map of CA School Districts

  // TODO create Chart/Synopsis of current directory

  // TODO Create Results Table

  // Table Example:
  // http://bl.ocks.org/llimllib/841dd138e429bb0545df

  // TODO: move this to template
  document.write('<link href="//cdn.muicss.com/mui-0.9.41/css/mui.min.css" rel="stylesheet" type="text/css" />');
  document.write('<script src="//cdn.muicss.com/mui-0.9.41/js/mui.min.js"></script>');

  var button = d3
    .select("body")
    .append("button")
    .text("hello")
    .classed("mui-btn mui-btn--primary mui-btn--raised", true);

  appendFullDataTable();

  // TODO connect each row to load detail in Synopsis
}

main();
