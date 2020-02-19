<template>
    <div>
        <div id="tooltip"></div>
        <svg id="map"></svg>
        <div id="announce">
            <span class="badge">🛡</span>
            New Achievement Unlocked for Open San Diego!
        </div>
        <p> HI PEOPLE </p>
    </div>
</template>

<script>
import _ from 'lodash';
import usa_topojson from 'us-atlas/states-albers-10m.json';
import * as d3 from 'd3';
import * as topojson from 'topojson';
import * as us from 'us';

export default {
  data() {
      return{
          statedata: {
              ca: {}
          }
      }
  },
   mounted(){
       this.createMap();
    //    this.updateMap();
   },
   methods: {
       createMap(){
            const svg = d3.select("#map")
              .attr("viewBox",[[0,0],[975,610]]); 
            const path = d3.geoPath();

            console.log("making map of ",usa_topojson,svg)
            svg.append("g")
                  .attr("class", "states")
                .selectAll("path")
                .data(topojson.feature(usa_topojson, usa_topojson.objects.states).features)
                .enter().append("path")
                  .attr("d", path)
                  .attr("fill", d => {
                       const state = us.lookup(d.id)     
                       if (this.statedata[state.abbr.toLowerCase()]){
                           return "green"
                       }else{
                           return "gray"
                       }
                  }

                  )
                  .attr("name", d=> d.name)
                  .on("click", d => {
                            d3.select("#tooltip").style("opacity",0);
                            
                              const state = us.lookup(d.id)
                            console.log("Hello", state)
                            if(this.statedata[state.abbr.toLowerCase()]){
                                this.$router.push(`/explore/${state.abbr.toLowerCase()}`)
                            }else{
                                // TODO pop up modal instead?
                                alert("Sorry, this state's data is not yet available")
                            }
                            })  
       },
       updateMap(){
            const projection = d3.geoAlbersUsa().scale(1280).translate([975/2, 610/2])
            const brigade_r = 10;
            console.log("updating map with",this.brigades);

            const color3= d3.scaleLinear()
                .domain([0,1])
                .range(['#fedd44','#00a175'])
                .interpolate(d3.interpolateHcl); 

            d3.select("#map").select(".brigades")
                .selectAll("circle") 
                .data(this.brigades, d => d.name )
                .join(
                    enter => enter.append("circle")
                        .attr("r", d => d.projects.length == 0?2:brigade_r)
                        .attr("transform", d => { 
                            var p = projection(
                                [d.longitude,d.latitude]
                            ); 
                            if(p){
                                return `translate( ${p[0]},${p[1]})`;
                            }else{
                                console.log("unable to place",d.name,d)
                                return `translate(-100,-100)`; // Sorry PR!
                            }
                        } )
                        .attr("fill", d => {
                            if(d.tagged == null){ return "lightgray" };
                            const p = d.tagged / d.projects.length;
                            return color3(p);
                        })
                        .on("mouseover", d => {
                            const div = d3.select("#tooltip")
                            div.transition().duration(200).style('opacity',.9);

                            div	.html(
                                `${d.name}` 
                                + `<br> ${d.projects.length } Projects ` 
                                + ((d.tagged==null)?"":`<br> ${d.tagged} have topics`)
                                ).style("left", (d3.event.pageX + brigade_r) + "px")		
                                .style("top", (d3.event.pageY - brigade_r) + "px");	
                        })			
                        .on("mouseout", d => {
                            const div = d3.select("#tooltip")
                            div.transition().duration(500).style('opacity',0);
                        })
                        .on("click", d => {
                            d3.select("#tooltip").style("opacity",0);
                            this.$router.push(`/brigade/${d.slug}`)
                            // TODO load Brigade Detail  
                        }),
                    update => update.attr("name",d => d.name)
                        .attr("r", d => d.projects.length == 0?2:brigade_r)
                        .attr("fill", d => {
                            if(d.tagged == null){ return "lightgray" };
                            const p = d.tagged / d.projects.length;
                            return color3(p);
                        }),
                )
       },
   }
}
</script>

<style>
#map {
    width: 75%;
    display: block;
    margin: 100px auto;
}
.states path {
    /* fill: #399fd3; */
    stroke: #fff;
    stroke-width: 1px;
}

.brigades circle {
    stroke: #444444;
    stroke-width: 1px;
    cursor: pointer;
    transition: r 200ms, fill 200ms;
}

#tooltip {
    border-radius: 3px;
    position: absolute;
    padding: 8px;
    background-color: white;
    border: solid 1px black;
    min-width: 100px;
    min-height: 100px;
    opacity: 0;
    pointer-events: none;
}

#announce {
    position: absolute;
    width: 50%;
    top: 40%;
    left: 25%;
    margin: auto;
    min-height: 100px;
    background-color: #fedd44;
    border: solid 3px white;
    border-radius: 10px;
    padding: 20px;
    font-size: 32pt;
    opacity: 0;
    display: none; 
}
#announce .badge {
    font-size: 100px; 
    vertical-align: middle;
}

</style>