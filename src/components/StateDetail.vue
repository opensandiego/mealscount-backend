<template>
    <section class="state-detail container my-3">
        <div class="row">
            <h1 class="col-sm-6">{{ state.name }}</h1>
            <div class="district-filter col-sm-2 offset-sm-4 "><input type="text" placeholder="Filter Districts" v-model="district_filter" /></div>
        </div>
        <div class="row">
            <table  @mouseover="hover = true" @mouseleave="hover = false" class="table col-sm district-table">
              <thead class="thead-dark">
                <tr>
                  <th scope="col" @click="set_sort('code')">District Code</th>
                  <th scope="col" @click="set_sort('name')">District Name</th>
                  <th scope="col" @click="set_sort('school_count')">Schools</th>
                  <th  v-tooltip title="Placeholder!" scope="col" @click="set_sort('total_enrolled')">Total Enrolled</th>
                  <th v-tooltip title="Placeholder!" scope="col" @click="set_sort('overall_isp')">Overall ISP</th>
                  <th v-tooltip title="Based on 180 days in school year">Est. Reimbursement <sup>1</sup></th>
                  <th v-tooltip title="Placeholder!" >Best Strategy</th>
                </tr>
              </thead>



              <tbody>
                <tr v-for="district in districts" v-bind:key="district.code">
                  <td>
                    {{ district.code }}
                  </td>
                  <td>
                    <router-link :to="{name:'district-detail', params: {state_code:'ca',district_code: district.code} }" >{{ district.name }}</router-link>
                  <td>{{ district.school_count }}</td>
                  <td>{{ district.total_enrolled.toLocaleString() }}</td>
                  <td>{{ (district.overall_isp * 100).toFixed(1) }}%</td>
                  <td>{{ (district.est_reimbursement * 180) | toUSD }}</td>
                  <td>{{ district.best_strategy }}</td>
                </tr>
              </tbody>
            </table>
        </div>
    </section>
</template>

<script >
import VTooltip from 'v-tooltip';

export default {
    props: ['state_code'] ,
    data() {
      return {
        sort_col: "total_enrolled",
        msg: "Hello",
        sort_desc: true,
        district_filter: '',
        use: VTooltip,
      }
    },
    
    computed: {
        state() {
            // Todo buld from state_cod
            return {name:"California",code:this.state_code};
        },
        districts(){
          const districts =_.orderBy(this.$store.getters.districts, [this.sort_col], [this.sort_desc?"desc":"asc"]);
          if( this.district_filter.length > 2){
            return _.filter(districts, d => d.name.toLowerCase().includes(this.district_filter.toLowerCase()))
          }
          return districts;
        }
    },
    methods: {
      set_sort(col){
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