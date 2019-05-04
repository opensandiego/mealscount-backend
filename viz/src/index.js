import _ from 'lodash';
import './style.css';
import * as d3 from 'd3';

function main() {

    d3.json("data.json").then(function(data){
        console.log("Data",data);

        // TODO create Map of CA School Districts

        // TODO create Chart/Synopsis of current directory

        // TODO Create Results Table

        // Table Example:
        // http://bl.ocks.org/llimllib/841dd138e429bb0545df 

        var table = d3.select("body").append("table").attr("border","1");
        var thead = table.append("thead");
        var tbody = table.append("tbody");

        thead.append("th").text("District");
        thead.append("th").text("Code");
        thead.append("th").text("Total enrolled");
        thead.append("th").text("# Schools");
        thead.append("th").text("ISP Best");

        var tr = tbody.selectAll("tr")
                    .data(data)
                    .enter().append("tr");

        var td = tr.selectAll("td")
                    .data(function(d) { return [d.district, d.code, d["total enrolled"], d["# schools"],d["ISP Best"]]; })
                    .enter().append("td")
                    .text(function(d) { return d; });
        
        // TODO connect each row to load detail in Synopsis

    });

}

main();
