<template>
     <table class="table col-sm school-table">
        <thead class="thead-dark">
          <tr id="district-table-header">
            <th scope="col" v-tooltip title="Best grouping by number based upon current optimization" @click="set_sort('grouping')">Recommended Grouping <img v-bind:src="image.qmark"></th>
            <th scope="col" @click="set_sort('school_code')">School Code</th>
            <th scope="col" @click="set_sort('school_name')">School Name</th>
            <th scope="col" v-tooltip title="School type (charter vs public) based on CALPAS (may not be accurate)">School Type <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Total students enrolled" scope="col" @click="set_sort('total_enrolled')">Total Enrolled <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Total Eligible. Default data is derived from Direct Certified only" scope="col" @click="set_sort('total_eligible')" >
              Total Eligible <sup>2</sup> <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="From average meals per day April 2019, based upon CFPA SNP Report" scope="col">
              Daily Breakfast Served
              <sup>3</sup> <img v-bind:src="image.qmark">
            </th>
            <th  v-tooltip title="From average meals per day April 2019, based upon CFPA SNP Report" scope="col">
              Daily Lunch Served
              <sup>3</sup> <img v-bind:src="image.qmark">
            </th>
            <th v-tooltip title="Whether or not this school is included in the algorithm" scope="col" @click="set_sort('active')">Included in Optimization <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Current ISP based upon total eligible / total enrolled" scope="col" @click="set_sort('isp')">School ISP <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Whether or not the ISP is above the CEP threshold for this school alone" scope="col">School CEP Eligible <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Reimbursement per school year" scope="col">Reimbursement Per School </th>
          </tr>
        </thead>
        <tbody v-if="editMode">
          <SchoolRowEdit 
            v-for="school in ordered_schools" 
            v-bind:key="school.school_code" 
            v-bind:school="school"
          />
          <AddSchoolRow 
            @add_school="add_school"
          />
        </tbody>
        <tbody v-else>
          <SchoolRow 
            v-for="school in ordered_schools" 
            v-bind:key="school.school_code" 
            v-bind:school="school"  
            v-bind:group="best_group_index[school.school_code]" 
            v-bind:color="color_for(school)"
          />
        </tbody>
          <!--
          <tr v-if="editMode == true" class="add_row">
            <td>Add School:</td>
            <td><input type="text" v-model="new_school_to_add.code" name="school_code" placeholder="School Code" /></td>
            <td><input type="text" v-model="new_school_to_add.name" name="school_name" placeholder="School Name" /></td>
            <td><input type="text" v-model="new_school_to_add.type" name="school_type" value="Public" /></td>
            <td colspan="7"><button v-on:click="add_school" class="btn btn-primary">Add</button></td>
          </tr> -->
      </table>   
</template>

<script>
import SchoolRow from "./SchoolRow.vue"
import SchoolRowEdit from "./SchoolRowEdit.vue"
import AddSchoolRow from "./AddSchoolRow.vue"
import QUESTION from '../../assets/qmark.png'
import * as chroma from 'chroma-js'

export default {
  props: ['schools','best_group_index','editMode'] ,
  data() {
    return {
      image: {qmark: QUESTION},
      sort_col: "grouping",
      sort_desc: false,
    }
  },
  components: {
    SchoolRow,
    SchoolRowEdit,
    AddSchoolRow
  },
  computed: {
    ordered_schools() {
      this.schools.forEach(s => {
        s.grouping = this.best_group_index[s.school_code];
      });
      return _.orderBy(
        this.schools,
        [this.sort_col],
        [this.sort_desc ? "desc" : "asc"]
      );
    },
    colorScale(){
      // See options here https://gka.github.io/chroma.js/#scale-correctlightness
      return chroma.scale('Set3').domain([0,Object.keys(this.best_group_index).length]); 
    }
  },
  methods:{
    set_sort(col) {
      if (col == this.sort_col) {
        this.sort_desc = !this.sort_desc;
      } else {
        this.sort_col = col;
        this.sort_desc = false;
      }
    },
    color_for(school){
      if( school.school_code in this.best_group_index){
        return this.colorScale( this.best_group_index[school.school_code] ).alpha(0.5)
      }else{
        return 'transparent'
      }
    },
    add_school(school){
      console.log("Adding School: ", school)
      this.schools.push(school);
    }
  }
}
</script>

<style scoped>
table.school-table {
  position: relative;
}
.school-table th {
  position: sticky;
  top: 45px;
}

</style>