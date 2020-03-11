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
            <div class="row" v-for="(scenario,index) in scenarios" v-bind:key="index">
                <div class="col-sm-6">{{ scenario.name }}</div>
                <div class="col-sm-2">
                  <button
                  class="btn"
                  @click="load_scenario(index)"
                  >Load</button>
                </div>
                <div class="col-sm-2">
                  <button
                  class="btn"
                  @click="delete_scenario(index)"
                  >Delete</button>
                </div>
            </div>

            <div class="col-sm-12">
              Scenario Name:
              <input type="text" v-model="new_scenario_name" v-bind:class="{error: isValidName}" />
            </div>
            <div class="col-sm-12">
              <button
                v-bind:disabled="!isValidName"
                class="btn btn-primary"
                @click="save_scenario" 
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
          new_scenario_name: "",
        }
    },
    computed:{
      scenarios(){
        return this.$store.getters.get_scenarios;
      },
      isValidName(){
          return /[\w-_]{3,}/.test(this.new_scenario_name);
      }
    },
    methods: {
        save_scenario(){
          this.$store.dispatch("save_scenario", {name:this.new_scenario_name, district:this.district});
        },
        load_scenario(i){
          this.$store.dispatch("load_scenario", i );
        },
        close() {
          this.$emit("close");
        },
        delete_scenario(i) {
          if(window.confirm("Delete Scenario " + this.scenarios[i].name + "?")){
            this.$store.dispatch("delete_scenario", i);
          }
        },
    }
}
</script>