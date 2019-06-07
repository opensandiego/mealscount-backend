var SCHOOL_YEAR = 180; // Days in school year

// Define Filters
Vue.filter("ispFormat", function(v){ return "" + (v*100).toFixed(1) + "%"; });
// Commas regex from https://stackoverflow.com/questions/2901102/
Vue.filter("commas", function(v){ return v.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); });
Vue.filter("deltaCommas", function(v){ 
    var x = v.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); 
    if(v > 0){ return "+"+x; }
    return x;
    
});
Vue.filter("money", function(v){ 
    var prefix = "$";
    if(v > 0){ prefix = "+$"; }
    else if(v < 0){ prefix = "-$"; }
    var x = Math.abs(v).toFixed(2);
    if( x >=  1000000000){
        return prefix + (x/1000000000).toFixed(2) + "b";
    }else if( x >= 1000000){
        return prefix + (x/1000000).toFixed(1) + "m";
    }else{
        return prefix + (x/1000).toFixed(1) + "k";
    }
    
});

// Our base data object 
var data = {district_data:[], filter:"",selected:null,SCHOOL_YEAR:SCHOOL_YEAR};
// Our Vue App
var app = new Vue({
    el: '#app',
    data: data,
    computed: {
        // Compute filtered districts to display
        districts: function(){
            return data.district_data.filter(function(o){ 
                if( data.filter == "" ){ return true; }  
                if( o.name.toLowerCase().search(data.filter.trim().toLowerCase()) >= 0 ||
                    o.code.toLowerCase().indexOf(data.filter.trim().toLowerCase()) == 0){
                    return true;
                }
                return false;
            });
        },
        summary: function(){
            var result = {
                total_enrolled:0,
                potential_improvement:0,
                potential_reimbursement:{low:0,high:0,delta:0}
            }; 
            data.district_data.forEach(function(d){
                result.total_enrolled += d.total_enrolled;
                result.potential_improvement += d.strategies[d.best_index].total_eligible - d.strategies[0].total_eligible;
                result.potential_reimbursement.low += d.strategies[d.best_index].reimbursement.low_end_estimate * SCHOOL_YEAR;
                result.potential_reimbursement.high += d.strategies[d.best_index].reimbursement.high_end_estimate * SCHOOL_YEAR;
                result.potential_reimbursement.delta += 
                    ( d.strategies[d.best_index].reimbursement.high_end_estimate - d.strategies[0].reimbursement.high_end_estimate ) * SCHOOL_YEAR;
            });
            return result;
        }
    },
    methods: {
        // select district when clicked
        selectDistrict: function(d) {
            data.selected = d;
            console.log(d);
            
            // highlight and center on the map
            map.mapLayer.selectAll('path').style('fill','#eeeeee');
            var d3_district = map.mapLayer.select('#map_district_'+d.code)
            d3_district.style('fill','#0000ff');
        },
        deselectDistrict: function(){
            console.log("deselecting");
            data.selected = null;
            // summary does not come back
            create_summary('#summary',300,100);
        },
        increaseOverBaseline: function(s,base){
            return s.total_eligible - base.total_eligible;
        },
        increaseReimbursementOverBaseline: function(s,base){
            // CONSIDER ok to show maximal range here?
            return [ s.reimbursement.low_end_estimate - base.reimbursement.low_end_estimate,
                     s.reimbursement.high_end_estimate - base.reimbursement.high_end_estimate ];
        }
    } 
})

// Retrieve our district data, and sort by largest first
var request = new XMLHttpRequest();
request.open('GET', 'output.json', true);
request.onload = function() { 
    data.district_data = JSON.parse(request.responseText); 
    data.district_data.sort(function(a,b){ return b.total_enrolled - a.total_enrolled} );

    create_map('#map',300,350);
    //create_summary('#summary',300,100);
}
request.send();

// Use D3 to render a map of California
var map = {};
function create_map(selector,width,height){
    map.projection = d3.geoMercator()
                            .scale(1400)
                            .center([-119,37])
                            .translate([width / 2, height / 2]);
    var path = d3.geoPath()
                    .projection(map.projection);

    var svg = d3.select(selector)
                .attr('width', width)
                .attr('height', height); 
    
    map.g = svg.append('g');

    map.mapLayer = map.g.append('g')
        .classed('map-layer', true);

    var tracts = d3.json('data/ca_districts.geojson');
    tracts.then(function(mapData) {
        map.data = mapData.features;
        console.log(map.data);

        // TODO colorize by  increase
        map.mapLayer.selectAll('path')
            .data(mapData.features)
            .enter().append('path')
                .attr('id', function(d){ return "map_district_"+d.properties.code; })
                .attr('lat', function(d){ return d.properties.INTPTLAT; })
                .attr('lng', function(d){ return d.properties.INTPTLON; })
                .attr('d', path)
                .attr('vector-effect', 'non-scaling-stroke')
                .on('click',function(d){
                    var district = data.district_data.filter(function(o){
                        return o.code == d.properties.code;
                    })[0];
                    app.selectDistrict(district);
                })
                .style('fill', "#eeeeee")
                .style('stroke',"#aaaaaa")
                .style('stroke-width','0.25')

    });
}

function create_summary(selector,overall_width,overall_height){

    var margin = 10;
    var width = overall_width - (margin*2);
    var height = overall_height - (margin*2);

    // calculate some stats
    var max_enrolled = data.district_data[0].total_enrolled;
    var min_enrolled = data.district_data[data.district_data.length-1].total_enrolled;

    var isps = data.district_data.map(function(o){ return o.overall_isp; }).sort();
    var max_isp = isps[isps.length -1 ];
    var min_isp = isps[0] 

    var svg = d3.select(selector)
                    .attr('width',width)
                    .attr('height',height)
                    .attr("transform",
                    "translate(" + margin + "," + margin + ")");
  
    var x = d3.scaleLinear()
        .domain([min_enrolled,max_enrolled])
        .range([0,width]);
    svg.append("g")
        .attr("transform", "translate(0,"+height+")")
        .call(d3.axisBottom(x));
    var y = d3.scaleLinear()
        .domain([min_isp*100,max_isp*100])
        .range([ height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));
    svg.append('g')
        .selectAll("dot")
        .data(data.district_data)
        .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.total_enrolled); } )
            .attr("cy", function (d) { return y(d.overall_isp*100); } )
            .attr("r", 2)
            .style("fill", "#0000ff33" )
}


