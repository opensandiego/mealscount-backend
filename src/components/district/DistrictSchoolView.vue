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
            <th v-tooltip title="Averaged site-level claiming data from April 2019, based upon CFPA SNP Report" scope="col">
              Breakfast Avg Daily Participation (ADP)
              <sup>3</sup> <img v-bind:src="image.qmark">
            </th>
            <th  v-tooltip title="Averaged site-level claiming data from April 2019, based upon CFPA SNP Report" scope="col">
              Lunch Avg Daily Participation (ADP)
              <sup>3</sup> <img v-bind:src="image.qmark">
            </th>
            <th v-tooltip title="Whether or not this school is included in the algorithm" scope="col" @click="set_sort('active')">Included in Optimization <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Estimated ISP based upon total eligible / total enrolled listed" scope="col" @click="set_sort('isp')">Estimated School ISP <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Whether or not the ISP is above the CEP threshold for this school alone" scope="col">School CEP Eligible <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Estimated reimbursement per school year" scope="col">Estimated Reimbursement Per School </th>
          </tr>
        </thead>
        <tbody v-if="editMode">
          <SchoolRowEdit 
            v-for="school in ordered_schools" 
            v-bind:key="school.school_code" 
            v-bind:school="school"
            @remove="remove_school(school)"
          />
          <AddSchoolRow 
            @add_school="add_school"
          />
        </tbody>
        <tbody v-else-if="ordered_schools.length > 0">
          <SchoolRow 
            v-for="school in ordered_schools" 
            v-bind:key="school.school_code" 
            v-bind:school="school"  
            v-bind:group="best_group_index[school.school_code]" 
            v-bind:color="color_for(school)"
          />
        </tbody>
        <tbody v-else>
          <tr>
            <td class="text-center" colspan="12">
              <button class="btn btn-primary" @click="$emit('toggleEdit')">Begin Adding Schools!</button>
            </td>
          </tr>
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
        if(s.school_code in this.best_group_index){
          s.grouping = this.best_group_index[s.school_code];
        }else{
          s.grouping = null;
        }
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
    },
    remove_school(school){
      if(window.confirm("Remove School  " + school.school_name + " ("+school.school_code + ")?")){
        const i = this.schools.indexOf(school);
        this.schools.splice(i,1)
      }
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