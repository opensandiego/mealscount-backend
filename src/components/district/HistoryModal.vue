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
            <strong>District Edit History</strong>

            <button type="button" class="btn-close" @click="close" aria-label="Close modal">x</button>
          </slot>
        </header>
        <section class="modal-body" id="modalDescription">
          <slot name="body">
            <h3>District Grouping History</h3>
            <p>These are the groupings you have run for District "{{ district_code }}" this session. Click on one to go back to it. <strong>Your current revision will still be available until you close this browser.</strong></p>
            <p>To save a revision, please use <em>Export to CSV</em></p>
            <ul>
                <li class="revision" v-for="edited in history" v-bind:key="edited.revision">
                    Revision #{{ edited.revision }} 
                    {{ (edited.est_reimbursement * schoolDays) | toUSD }}
                    {{ edited.strategies[edited.best_index].covered_students }}

                    <span v-if="edited.revision == current_revision">(current)</span>

                    <button
                        class="btn btn-primary active btn-sm"
                        type="button"
                        data-toggle="button"
                        aria-pressed="false"
                        autocomplete="off"
                        v-on:click="load_district(edited.revision)"
                    >Load</button>
                </li>
            </ul>
          </slot>
        </section>
        <footer class="modal-footer">
          <slot name="footer">
            <button
              type="button"
              class="btn-green"
              @click="close"
              aria-label="Close modal"
            >Cancel</button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: ["district_code","state_code","schoolDays","current_revision"],
  computed: {
    history(){
      return this.$store.getters.get_history(this.state_code,this.district_code)
    }
  },
  methods: {
    close() {
        this.$emit("close");
    },
    load_district(district_revision){
        this.$store.dispatch("load_district_revision", district_revision)
        this.$emit("close");
    }
  }
};
</script>

<style scoped>
li.revision {
    margin-bottom: 10px;
}
</style>