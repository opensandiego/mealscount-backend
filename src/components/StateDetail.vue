<template>
    <section class="state-detail container my-3">
        <div class="row">
            <h1 class="col-sm">{{ state.name }}</h1>
        </div>

        <div class="row">
            <table class="table col-sm">
              <thead class="thead-dark">
                <tr>
                  <th scope="col" @click="set_sort('code')">District Code</th>
                  <th scope="col" @click="set_sort('name')">District Name</th>
                  <th scope="col" @click="set_sort('schools.length')">Schools</th>
                  <th scope="col" @click="set_sort('total_enrolled')">Total Enrolled</th>
                  <th scope="col" @click="set_sort('overall_isp')">Overall ISP</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="district in districts" v-bind:key="district.code">
                  <td>
                    {{ district.code }}
                  </td>
                  <td>
                    <router-link :to="{name:'district-detail', params: {state_code:'ca',district_code: district.code} }" >{{ district.name }}</router-link>
                  <td>{{ district.schools_count }}</td>
                  <td>{{ district.total_enrolled.toLocaleString() }}</td>
                  <td>{{ (district.overall_isp * 100).toFixed(1) }}%</td>
                </tr>
              </tbody>
            </table>
        </div>
    </section>
</template>

<script>
export default {
    props: ['state_code'] ,
    data() {
      return {
        sort_col: "total_enrolled",
        sort_desc: true,
      }
    },
    computed: {
        state() {
            // Todo buld from state_cod
            return {name:"California",code:this.state_code};
        },
        districts(){
            return _.orderBy(this.$store.getters.districts, [this.sort_col], [this.sort_desc?"desc":"asc"]);
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
  .state-detail .table th {
    cursor: pointer;
  }
</style>