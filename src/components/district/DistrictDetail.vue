<template>
  <section class="state-detail my-3" v-if="district != null">
    <div class="container">
      <div class="row">
        <div class="container">
          <router-link
            :to="{name:'state-detail', params: {state:state_code} }"
          >&laquo; Back to state</router-link>
        </div>
      </div>

      <div class="row">
        <h1 class="col-sm">{{ district.name }} ({{ district_code }} - {{ state_code }})</h1>
      </div>

      <DistrictSummary v-bind:district="district" v-bind:schoolDays="schoolDays" v-bind:editMode="editMode" />

      <ScenarioControl />
    </div>

    <div class="row">
      <div class="col-sm">
        <div class="alert alert-primary" role="alert">
          <strong>PLEASE NOTE</strong>
          The data shown for this district is from the 2018-2019 CALPADS aggregate data, as well as April 2019 meals average meals data.
          ISP numbers are for <strong>Direct Certification Only</strong>. Your district's numbers may be significantly higher. 
          Some charter schools may be included, and some preschool schools may be missing, based upon the school data we receive from CALPADS.
          To get the best recommended grouping, the school listing and ISP numbers should be modified to match the reality of your school.
          For more information or questions, please <router-link to="/contact">Contact Us</router-link>!
        </div>
      </div>
    </div>

    <div class="row container mx-auto" v-if="district != null && viewMode == 'group'">
        <DistrictGroupView v-bind:district="district" />
    </div>

    <div class="row px-3" v-if="district != null && viewMode == 'table'">
        <div class="col-sm-12">
              <button
                v-if="editMode == false"
                class="btn btn-primary"
                type="button"
                data-toggle="button"
                aria-pressed="false"
                autocomplete="off"
                v-on:click="toggleEdit"
              >edit</button>
              <button
                v-if="editMode == true"
                class="btn btn-primary"
                type="button"
                data-toggle="button"
                aria-pressed="true"
                autocomplete="off"
                v-on:click="submit"
              >submit</button>
              <button
                v-if="editMode == true"
                class="btn btn-primary"
                type="button"
                data-toggle="button"
                aria-pressed="true"
                autocomplete="off"
                v-on:click="toggleEdit"
              >cancel</button>

              <span class="badge badge-secondary" v-if="edited">Edited, refresh to clear</span>
              </div>
        <DistrictSchoolView v-bind:schools="district.schools" v-bind:best_group_index="best_group_index" v-bind:editMode="editMode" />
    </div>

    <div>
      <sup>1</sup>
      Based on {{ schoolDays }} days in school year
      <br />
      <sup>2</sup>Derived from Direct Certified only
      <br />
      <sup>3</sup>From average meals per day April 2019, based upon CFPA SNP Report
      <br />
    </div>
  </section>
</template>

<script>
import * as _ from "lodash";
import DistrictSummary from "./DistrictSummary.vue"
import ScenarioControl from "./ScenarioControl.vue"
import DistrictSchoolView from "./DistrictSchoolView.vue"
import DistrictGroupView from "./DistrictGroupView.vue"

// TODO "404" if no district?
// TODO break this down into little components...
export default {
  components: {
    DistrictSummary,
    ScenarioControl,
    DistrictSchoolView,
  },
  props: ["state_code", "district_code"],
  data() {
    return {
      school_form: null,
      district_form: {},
      editMode: false,
      viewMode: "table", // or "group"
      schoolDays: 180,
      new_school_to_add: {
        code:'',name:'',type:''
      },
    };
  },
  computed: {
    district() {
      return this.$store.getters.selected_district;
    },
    edited(){
      return this.district != null && this.district.edited != undefined;
    },
    grouped_schools() {
      if (this.district == null || this.district == null) {
        return [];
      }
      const s = this.district.strategies[this.district.best_index];
      const grouped = [];
      const schools = this.district.schools;
      var i = 1;
      s.groups.forEach(g => {
        const group = {
          id: i,
          data: g,
          schools: _.filter(schools, s => {
            return g.school_codes.indexOf(s.school_code) >= 0;
          })
        };
        i++;
        grouped.push(group);
      });
      return _.orderBy( grouped, ['data.isp'], 'desc');
    },
    best_strategy() {
      if (this.district == null || this.district == null) {
        return null;
      }
      if (!this.district.strategies) {
        return null;
      }
      return this.district.strategies[this.district.best_index];
    },
    best_group_index() {
      if (this.best_strategy == null) {
        return null;
      }
      const group_index = {};
      var i = 1;
      this.best_strategy.groups.forEach(g => {
        g.school_codes.forEach(sc => {
          group_index[sc] = i;
        });
        i += 1;
      });
      return group_index;
    }
  },
  watch: {
    district( newVal, oldVal) {
      if(newVal != null){
        this.init_school_form();
        // Set district meta data
        _.defaultsDeep(this.district_form,{'reimbursement_rates':this.district.rates});
        this.district_form.code = this.district_code;
        this.district_form.name = this.district.name;
        this.district_form.state_code = this.state_code;
      }
    }
  },

  methods: {
    init_school_form(){
      console.log("adding schools");
      this.school_form = {};
      this.district.schools.forEach(school => {
          this.school_form[school.school_code] = {
            name: school.school_name,
            code: school.school_code,
            type: school.school_type,
            total_enrolled: school.total_enrolled,
            total_eligible: school.total_eligible,
            daily_breakfast_served: school.daily_breakfast_served,
            daily_lunch_served: school.daily_lunch_served,
            active: school.active
          };
      });
    },
    save_school_data(name){
      const data = JSON.stringify(this.district.schools);
      localStorage.setItem(name,data);
      if( !_.includes(this.scenarios,name) ){
        this.saved_scenarios.push(name);
        this.save_scenario_list();
      }
    },
    load_school_data(name){
      if(localStorage.getItem(name)){
        try{
          // preserve initial loaded data
          if(! this.district.original_schools){
            this.district.original_schools = this.district.schools;
          }
          this.district.schools = JSON.parse(localStorage.getItem(name));
          this.scenario_name = name;
          this.init_school_form();
          if(!this.editMode){
            this.toggleEdit()
          }
          console.log("loaded ",name)
        }catch(e){
          console.error("Couldn't load scenario",name,e);
          localStorage.removeItem(name);
          this.saved_scenarios = _.pull(this.saved_scenarios,[name]);
          this.save_scenario_list();
        }
      }else{
        console.log("clearning missing scenario:",name)
        this.saved_scenarios = _.filter(this.saved_scenarios, v => v != name );
        this.save_scenario_list();
      }
    },
    save_scenario_list(){
      const data = JSON.stringify(this.saved_scenarios);
      localStorage.setItem('scenarios',data);
    },
    handle_save_scenario(){
      if(!this.scenario_name){
        alert("Please enter a scenario name");
        return;
      }
      this.save_school_data(this.scenario_name);
    },
    handle_load_scenario(){
      if(!this.scenario_to_load){
        alert("Please select a scenario to load");
        return;
      }
      this.load_school_data(this.scenario_to_load);
    },
    toggleEdit() {
      this.editMode = !this.editMode;
    },
    submit(){
      console.log("Submitting for optimization",this.school_form,this.district_form) 
      const district_info = {
        schools: this.school_form,
        code: this.district_form.code,
        name: this.district_form.name,
        state_code: this.district_form.state_code,
        reimbursement_rates: this.district_form.reimbursement_rates,
      }
      // TODO add reimbursement rates, % increase, SFA Cert
      this.$store.dispatch("run_district",district_info);
    },
    add_school(){
      const new_school = {
        name: this.new_school_to_add.name,
        code: this.new_school_to_add.code,
        type: this.new_school_to_add.type,
        total_enrolled: 1,
        total_eligible: 1,
        daily_breakfast_served: 1,
        daily_lunch_served: 1,
        active: true
      }
      if(this.school_form[new_school.code]){
        alert("School with this code already exists, please edit that row");
        return;
      }
      this.school_form[new_school.code] = new_school;
      // TODO unify school_form and district_data?
      const school_data = {
        school_name: this.new_school_to_add.name,
        school_code: this.new_school_to_add.code,
        school_type: this.new_school_to_add.type,
        active: true,
        total_enrolled: 1,
        total_eligible: 1,
        grouping: null,
        isp: 1,
        daily_breakfast_served: 1,
        daily_lunch_served: 1,
      }
      this.district.schools.push( school_data );
      // console.log("Adding to school_form",new_school);
      this.new_school_to_add.code='';
      this.new_school_to_add.name='';
      this.new_school_to_add.type='';
    },
    handleScroll (event) {
      const header = document.getElementById("district-table-header")
      const sticky = header.offsetTop;

      if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
      } else {
        header.classList.remove("sticky");
      }
    },
    daily_reimbursement_by_school ( school_code ){
      if(this.district_form.reimbursement_rates == null){
        return "";
      }
      return "?"

      // TODO - how do we determine group rate for this school?
      // if group ISP < 0.4, $0
      // if group ISP < 0.625, paid rate
      // else free rate
      const s = this.school_form[school_code];
      const v = ( s.daily_breakfast_served * this.district_form.reimbursement_rates.free_bfast ) 
                 + ( s.daily_lunch_served * this.district_form.reimbursement_rates.free_lunch )
      return v;
    },
  },
  created () {
    window.addEventListener('scroll', this.handleScroll);
  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll);
  }
};
</script>

<style scoped>
tr.inactive {
  font-style: italic;
  color: #999;
}
input {
  width: 4em;
}

tr.add_row {
  background-color: #eee;
}
tr.add_row td input {
  width: 100%;
}
table.school-table {
  position: relative;
}
.school-table th {
  position: sticky;
  top: 45px;
}
</style>