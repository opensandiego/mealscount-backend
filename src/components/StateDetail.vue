<template>
    <section class="state-detail container my-3" v-if="state != null">
        <div class="row">
            <h1 class="col-sm-6">{{ state.name }}</h1>
            <div class="district-filter col-sm-2 offset-sm-4 "><input type="text" placeholder="Filter Districts" v-model="district_filter" /></div>
            <div class="col-sm-12" v-html="state.about"></div>
        </div>
        <div class="row">
            <table  @mouseover="hover = true" @mouseleave="hover = false" class="table col-sm district-table">
              <thead class="thead-dark">
                <tr>
                  <th scope="col" @click="set_sort('code')">District Code</th>
                  <th scope="col" @click="set_sort('name')">District Name</th>
                  <th scope="col" @click="set_sort('school_count')">Schools</th>
                  <th v-tooltip title="The total number of students in this district" scope="col" @click="set_sort('total_enrolled')"> Total Enrolled <img v-bind:src="image.qmark"> </th> 
                  <th v-tooltip title="The total Identified Student Population (ISP) of this district" scope="col" @click="set_sort('overall_isp')">Overall ISP <img v-bind:src="image.qmark"> </th>
                  <th v-tooltip title="Based on 180 days in school year">Est. Reimbursement <sup>1</sup> <img v-bind:src="image.qmark"></th>
                  <th v-tooltip title="The algorithm that is producing the highest reimbursement rate" >Best Strategy <img v-bind:src="image.qmark"></th>
                </tr>
              </thead>



              <tbody v-if="districts.length > 0">
                <tr v-for="district in districts" v-bind:key="district.code">
                  <td>
                    {{ district.code }}
                  </td>
                  <td>
                    <router-link :to="{name:'district-detail', params: {state_code:'ca',district_code: district.code} }" >{{ district.name }}</router-link>
                  <td>{{ district.school_count }}</td>
                  <td>{{ district.total_enrolled.toLocaleString() }}</td>
                  <td>{{ (district.overall_isp * 100).toFixed(1) }}%</td>
                  <td class="text-right">{{ (district.est_reimbursement * 180) | toUSD }}</td>
                  <td><router-link to="/algorithms">{{ district.best_strategy }}</router-link></td>
                </tr>
              </tbody>
              <tbody v-else>
                <tr><td colspan="7">Loading districts</td></tr>
              </tbody>
            </table>
        </div>
    </section>
</template>

<script >
import VTooltip from 'v-tooltip';
import QUESTION from '../assets/qmark.png';
export default {
 
    props: ['state_code'] ,
    data() {
      return {
        sort_col: "total_enrolled",
        image: {qmark: QUESTION},
        sort_desc: true,
        district_filter: '',
        use: VTooltip,
      }
    },
    computed: {
        state() {
            return this.$store.getters.get_states[this.state_code];
        },
        districts(){
          if(!this.state){ return [] }
          const districts = _.orderBy(this.state.districts, [this.sort_col], [this.sort_desc?"desc":"asc"]);
          if(districts == null){ return [] }
          if( this.district_filter.length > 2){
            return _.filter(districts, d => d.name.toLowerCase().includes(this.district_filter.toLowerCase()))
          }
          return districts;
        }
    },
    methods: {
      set_sort(col){
        console.log("setting sor",col);
        if(col == this.sort_col){
          this.sort_desc = !this.sort_desc;
        }else{
          this.sort_col = col;
          this.sort_desc = false;
        }
      }

      
    }
}

</script>





<style scoped>

.tooltip {
  color: red;
  background: white;
}

.tooltip-arrow {
  color: red;
   z-index: 1;
}

  .state-detail .table th {
    cursor: pointer;
  }
  .state-detail .district-filter { 
    margin-top: 20px;
  }
  .state-detail .district-table {
    position: relative;
  }
  .state-detail .district-table th {
    position: sticky;
    top: 45px;
  }

  
</style>