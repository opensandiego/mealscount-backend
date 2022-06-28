<template>
  <div>
     <table class="table col-sm school-table">
        <thead class="thead-dark">
          <tr id="district-table-header">
            <th scope="col" 
                v-tooltip 
                title="Indicates the numerical grouping of the schools in the current recommendation. All Schools marked “1” should be in Group 1, all schools marked “2” should be in Group 2, etc. In the edit function, click “Remove” to remove a school from the school list before running the grouping calculation."
                @click="set_sort('grouping')">Recommended Grouping <img v-bind:src="image.qmark"></th>
            <th scope="col" @click="set_sort('school_code')">School Code</th>
            <th scope="col" @click="set_sort('school_name')">School Name</th>
            <th v-tooltip
                title="Pre-loaded data is based on the publicly available FRAC CEP file. Please edit with your updated enrollment data."
                scope="col" 
                @click="set_sort('total_enrolled')">Total Enrolled <img v-bind:src="image.qmark"></th>
            <th v-tooltip 
                title="Pre-loaded data is based on the publicly available FRAC CEP file. Please edit with your updated, de-duplicated count of all directly certified and categorically eligible students"
                scope="col" 
                @click="set_sort('total_eligible')" >
                Total Eligible <sup>2</sup> <img v-bind:src="image.qmark"></th>
            <th v-tooltip 
                title="Please edit based on your projected ADP." 
                scope="col">
                Breakfast Avg Daily Participation (ADP)
                <img v-bind:src="image.qmark">
                <div v-if="editMode">
                  <button @click="toggle_adp_modal(true)">Set as % enrolled</button>
                </div>
            </th>
            <th v-tooltip 
                title="Please edit based on your projected ADP." 
                scope="col">
                Lunch Avg Daily Participation (ADP)
                <img v-bind:src="image.qmark">
                <div v-if="editMode">
                  <button @click="toggle_adp_modal(true)">Set as % enrolled</button>
                </div>
            </th>
            <th v-tooltip 
                title="Severe Need" 
                scope="col" 
                >Severe Need</th>
            <th v-tooltip 
                title="Indicates whether a given school is run through the grouping calculation. Uncheck the box to exclude a given school from the grouping calculation." 
                scope="col" 
                @click="set_sort('active')">Included in Optimization <img v-bind:src="image.qmark"></th>
             <th v-tooltip 
                title="Estimated ISP based upon listed numbers of total eligible / total enrolled" scope="col" @click="set_sort('isp')">Estimated School ISP <img v-bind:src="image.qmark"></th>
            <th v-tooltip 
                title="Indicates whether a given school is eligible for CEP (at or above the 40% ISP threshold) without grouping." 
                scope="col">School CEP Eligible <img v-bind:src="image.qmark"></th>
            <th v-tooltip title="Estimated reimbursement per school year" scope="col">Estimated Annual Reimbursement Per School </th>
          </tr>
        </thead>
        <tbody v-if="editMode">
          <SchoolRowEdit 
            v-for="school in ordered_schools" 
            v-bind:key="school.school_code" 
            v-bind:school="school"
            v-bind:group_numbers="group_numbers"
            @remove="remove_school(school)"
          />
          <AddSchoolRow 
            ref="addSchoolRow"
            @add_school="add_school"
          />
        </tbody>
        <tbody v-else-if="ordered_schools.length > 0">
          <SchoolRow 
            v-for="school in ordered_schools" 
            v-bind:key="school.school_code" 
            v-bind:school="school"  
            v-bind:group="best_group_index[school.school_code]" 
            v-bind:reimbursement="reimbursement_index[school.school_code]"
            v-bind:group_numbers="group_numbers"
            v-bind:color="color_for(school)"
            @recalculate="$emit('recalculate')"
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
      <SetADPModal id="set_adp_modal"
        v-show="show_adp_set_modal"
        @close="toggle_adp_modal(false)"
        @apply="apply_adp_modal" />
  </div>
</template>

<script>
import SchoolRow from "./SchoolRow.vue"
import SchoolRowEdit from "./SchoolRowEdit.vue"
import SetADPModal from "./SetADPModal.vue"
import AddSchoolRow from "./AddSchoolRow.vue"
import QUESTION from '../../assets/qmark.png'
import * as chroma from 'chroma-js'

export default {
  props: ['schools','best_group_index','editMode','reimbursement_index'] ,
  data() {
    return {
      image: {qmark: QUESTION},
      sort_col: "grouping",
      sort_desc: false,
      show_adp_set_modal: false,
    }
  },
  components: {
    SchoolRow,
    SchoolRowEdit,
    AddSchoolRow,
    SetADPModal,
  },
  computed: {
    ordered_schools() {
      this.schools.forEach(s => {
        if(s.school_code in this.best_group_index){
          s.grouping = this.best_group_index[s.school_code];
        }else if(s.group){
          s.grouping = s.group;
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
    },
    group_numbers(){
      const groups = {} 
      this.schools.forEach(s=>{
        if(groups[s.grouping] == undefined){ groups[s.grouping] = 1 }
      })
      return Object.keys(groups).map( k => Number(k))
    },
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
      if( !school.school_code || this.schools.filter( s=> s.school_code == school.school_code ).length > 0){
        alert("Please enter a unique school code");
      }else{
        this.schools.push(school);
        this.$refs.addSchoolRow.clear();
      }
    },
    remove_school(school){
      if(window.confirm("Remove School  " + school.school_name + " ("+school.school_code + ")?")){
        const i = this.schools.indexOf(school);
        this.schools.splice(i,1)
      }
    },
    apply_adp_modal(adp){
      this.schools.forEach( s => {
        s.daily_breakfast_served = Math.round((adp.breakfast/100) * s.total_enrolled);
        s.daily_lunch_served = Math.round((adp.lunch/100) * s.total_enrolled);
      })
      this.show_adp_set_modal = false
    },
    toggle_adp_modal(show){
      this.show_adp_set_modal = show
    },
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