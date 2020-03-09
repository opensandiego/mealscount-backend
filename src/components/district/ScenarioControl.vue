<template>
      <div class="row">
        <div class="col-sm mb-3">
          Saved Scenarios
          <select v-model="scenario_to_load">
              <option v-for="scenario in saved_scenarios" v-bind:value="scenario" v-bind:key="scenario">{{ scenario }}</option>
          </select>
          <button v-on:click="handle_load_scenario">Load</button>
        </div>
        <!-- <div class="col-sm mb-3" v-if="school_form != null">
          <input type="text" id="save_scenario" v-model="scenario_name" placeholder="Scenario Name" /> 
          <button v-on:click="handle_save_scenario">Save Scenario</button>
        </div> -->
        <div class="col-sm mb-3">
          View By
          <select v-model="viewMode">
            <option value="group">Group</option>
            <option value="table">All Schools</option>
          </select>
        </div>
      </div>
</template>

<script>
export default {
    data(){
        return {
            scenario: null,
            scenario_name: '',
            saved_scenarios: [],
            scenario_to_load: null,
            viewMode: 'table',
        }
    },
    mounted() {
        if(localStorage.getItem('scenarios')){
          try{
            const parsed = JSON.parse(localStorage.getItem('scenarios'));
            console.log("setting parsed scenarios")
            this.saved_scenarios = parsed;
          }catch(e){
            console.log("issue loading scenarios",e);
            localStorage.removeItem("scenarios");
          }
        }
    },
    methods: {
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
    }

}
</script>