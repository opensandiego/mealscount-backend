<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div
        class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <header class="modal-header" id="modalTitle">
          <slot name="header">
            <strong>Saved Scenarios</strong>

            <button type="button" class="btn-close" @click="close" aria-label="Close modal">x</button>
          </slot>
        </header>
        <section class="modal-body" id="modalDescription">
          <slot name="body">

            <h3>Save / Load District Secenario</h3>

            <strong>Current Scenarios</strong>
            <div class="row" v-for="scenario in saved_scenarios" v-bind:key="scenario">
                <div class="col-sm-6">{{ scenario }}</div>
                <div class="col-sm-2">
                  <button>Load</button>
                </div>
                <div class="col-sm-2">
                  <button>Delete</button>
                </div>
            </div>

            <div class="col-sm-12">
              Scenario Name:
              <input type="text" v-bind:value="district.code + ' - ' + district.name" />
            </div>
            <div class="col-sm-12">
              <button
                class="btn btn-primary"
                @click="save" 
              >Save</button>
            </div>
          </slot>
        </section>
        <footer class="modal-footer">
          <slot name="footer">
            <button
              type="button"
              class="btn-green"
              @click="close"
              aria-label="Close modal"
            >Close me!</button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
    props: ['district'],
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
      this.load_scenario_list();
    },
    methods: {
        save_district(name){
          const data = JSON.stringify(this.district);
          localStorage.setItem(name,data);
          if( !_.includes(this.scenarios,name) ){
            this.saved_scenarios.push(name);
            this.save_scenario_list();
          }
        },
        load_scenario_list(){
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
        load_school_data(name){
          if(localStorage.getItem(name)){
            try{
              //this.district = JSON.parse(localStorage.getItem(name));
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
        save(){
          alert("not implemented")
        },
        load(){
          alert("not implemented")
        },
        close() {
          this.$emit("close");
        }
    }
}
</script>