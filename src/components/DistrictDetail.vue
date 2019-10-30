<template>
     <section class="state-detail container my-3" v-if="district != null">
        
        <div class="row">
            <h1 class="col-sm">{{ district.name }} ({{ district_code }} - {{ state_code }})</h1>
        </div>

        <div class="row">
            <dl class="col-sm">
                <dt>State</dt>
                    <dd>{{ state_code }}</dd>
                <dt>District Code</dt>
                    <dd>{{ district_code}}</dd>
                <dt>Total Enrolled</dt>
                    <dd>{{ district.total_enrolled }}</dd>
                <dt>Overall ISP</dt>
                    <dd>{{ (district.overall_isp*100).toFixed(1) }}%</dd>
                <dt>Estimated Reimbursement Range</dt>
                    <dd>TODO</dd>
            </dl>
        </div>

        <div class="row" v-if="district.data != null">
            <table class="table col-sm">
              <thead class="thead-dark">
                <tr>
                  <th scope="col">School Code</th>
                  <th scope="col">School Name</th>
                  <th scope="col">Total Enrolled</th>
                  <th scope="col">Overall ISP</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="school in district.data.schools" v-bind:key="school.code">
                  <td>{{ school.school_code }}</td>
                  <td>{{ school.school_name }}</td>
                  <td>{{ school.total_enrolled.toLocaleString() }}</td>
                  <td>{{ (school.isp * 100).toFixed(1) }}%</td>
                </tr>
              </tbody>
            </table>
        </div>
    </section> 
</template>

<script>
import * as _ from "lodash"

// TODO "404" if no district?
export default {
    props: ['state_code','district_code'],
    computed: {
        district(){
            var districts = _.filter(this.$store.getters.districts,d => d.code == this.district_code);
            if(districts.length){ return districts[0] }
            return null
        }
    },
    watch: {
        district(newVal,oldVal){
            if(this.district != null && this.district.data == null ){
                this.loadDistrictData();
            }
        }
    },
    mounted() {
        if(this.district != null && this.district.data == null){
            this.loadDistrictData();
        }
    },
    methods: {
        loadDistrictData(){
            this.$store.dispatch("load_district", {code:this.district_code,state:this.state_code})
        }
    }
}
</script>