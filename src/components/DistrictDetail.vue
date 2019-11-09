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
                    <dd>{{ district.total_enrolled.toLocaleString() }}</dd>
                <dt>Overall ISP</dt>
                    <dd>{{ (district.overall_isp*100).toFixed(1) }}%</dd>
                <dt>Estimated Annual Reimbursement Range<sup>1</sup></dt>
                    <dd v-if="best_strategy != null">
                        <strong>Winning Strategy:</strong> {{ best_strategy.name }}<br>
                        <strong>High:</strong> ${{ Math.round(best_strategy.reimbursement.high_end_estimate * 180).toLocaleString({ style: 'currency', currency: 'USD' }) }}<br>
                        <strong>Low:</strong> ${{ Math.round(best_strategy.reimbursement.low_end_estimate * 180).toLocaleString({ style: 'currency', currency: 'USD' }) }}<br>
                        <sup>1</sup>Based on 180 days in school year
                   </dd>
            </dl>
        </div>

        <div class="row" v-if="district.data != null">
            <table class="table col-sm">
              <thead class="thead-dark">
                <tr>
                  <th scope="col">School Code</th>
                  <th scope="col">School Name</th>
                  <th scope="col">School Type</th>
                  <th scope="col">Total Enrolled</th>
                  <th scope="col">Total Eligible</th>
                  <th scope="col">Daily Breakfast Served</th>
                  <th scope="col">Daily Lunch Served</th>
                  <th scope="col">Included in Optimization</th>
                  <th scope="col">Overall ISP</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="school in district.data.schools" v-bind:key="school.code">
                  <td>{{ school.school_code }}</td>
                  <td>{{ school.school_name }}</td>
                  <td>{{ school.school_type }}</td>
                  <td>{{ school.total_enrolled.toLocaleString() }}</td>
                  <td>{{ school.total_eligible.toLocaleString() }}</td>
                  <td>{{ school.daily_breakfast_served.toLocaleString() }}</td>
                  <td>{{ school.daily_lunch_served.toLocaleString() }}</td>
                  <td><span v-if="school.active">✔️</span></td>
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
        },
        best_strategy(){
            if(this.district == null || this.district.data == null){ return null; }
            if(!this.district.data.strategies){ return null; }
            return this.district.data.strategies[this.district.data.best_index]
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