import _ from "lodash";
import * as d3 from "d3";
import schoolMealData from "./data/data.json";

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
    .data(schoolMealData)
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

function showSchoolMealDataForCode(schoolMealItem) {
  var baselineISP = Math.round(schoolMealItem["ISP Baseline"] * 100) / 100;
  var bestISP = Math.round(schoolMealItem["ISP Best"] * 100) / 100;

  var card1text = "Baseline ISP: " + baselineISP + "% using strategy " + schoolMealItem["baseline"];
  d3.select(".district-info1").text(card1text);

  var card1text = "Best ISP: " + bestISP + "% using strategy " + schoolMealItem["best_strategy"];
  d3.select(".district-info2").text(card1text);
}

function generateDistrictSelector() {
  const listItems = d3
    .select(".district-list")
    .selectAll("li")
    .data(schoolMealData)
    .enter()
    .append("li");

  listItems.append("a").text(function(d, index) {
    return Object.assign(d.district, { index: index });
  });

  listItems.on("click", function(schoolMealItem) {
    showSchoolMealDataForCode(schoolMealItem);
  });

  // Show default first data item to start
  showSchoolMealDataForCode(schoolMealData[0]);
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
