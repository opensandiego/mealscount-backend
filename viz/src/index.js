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

function generateDistrictSelector() {
  d3.select(".district-list")
    .selectAll("li")
    .data(data)
    .enter()
    .append("li")
    .text(function(d) {
      return d.district;
    });

  // Show default first data item to start
  // TODO: make this dynamic hooking it up to the dropdown
  var dataRow = data[0];
  var baselineISP = Math.round(dataRow["ISP Baseline"] * 100) / 100;
  var bestISP = Math.round(dataRow["ISP Best"] * 100) / 100;

  var card1text = "Baseline ISP: " + baselineISP + "% using strategy " + dataRow["baseline"];
  d3.select(".district-info1")
    .append("div")
    .classed("mui--text-display1", true)
    .text(card1text);

  var card1text = "Best ISP: " + bestISP + "% using strategy " + dataRow["best_strategy"];
  d3.select(".district-info2")
    .append("div")
    .classed("mui--text-display1", true)
    .text(card1text);
}

function main() {
  // TODO create Map of CA School Districts

  // TODO create Chart/Synopsis of current directory

  generateDistrictSelector();

  // TODO Create Nicer Results Table

  // Table Example:
  // http://bl.ocks.org/llimllib/841dd138e429bb0545df
  appendFullDataTable();

  // TODO connect each row to load detail in Synopsis
}

main();
