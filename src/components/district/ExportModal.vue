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
            <strong>Export to CSV</strong>

            <button type="button" class="btn-close" @click="close" aria-label="Close modal">x</button>
          </slot>
        </header>
        <section class="modal-body" id="modalDescription">
          <slot name="body">
            <h3>Download {{ district.name }} as CSV</h3>
            <div class="col-sm-12">
              Filename:
              <input type="text" v-bind:value="download_filename" />
            </div>
            <div class="col-sm-12">
              <a
                v-bind:download="download_filename"
                class="btn btn-primary"
                v-bind:href="csv_data"
              >Download</a>
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
  props: ["district","grouping_index"],
  data() {
    return {
      download_filename: "district.csv"
    };
  },
  mounted() {
    this.download_filename =
      "mealscount-district-" + this.district.code + ".csv";
  },
  computed: {
    csv_data() {
      var x = "data:text/plain;charset=utf-8,";

      var csv_text = [
        "state",
        "district",
        "group",
        "school_code",
        "school_name",
        "total_enrolled",
        "total_eligible",
        "daily_breakfast_served",
        "daily_lunch_served",
        "included_in_optimization",
        "estimated_school_reimbursement"
      ].join(',') + '\n'

      this.district.schools.forEach( s => {
          csv_text += [
            this.district.state_code,
            this.district.code,
            (s.school_code in this.grouping_index)?this.grouping_index[s.school_code]:'',
            s.school_code,
            '"' + s.school_name + '"',
            s.total_enrolled,
            s.total_eligible,
            s.daily_breakfast_served,
            s.daily_lunch_served,
            s.active,
            'todo', // per-school-reimbursement
          ].join(',') + "\n"
      })

      x += encodeURIComponent(csv_text);
      return x;
    }
  },
  methods: {
    close() {
      this.$emit("close");
    }
  }
};
</script>

<style scoped>
input {
  width: 100%;
}
</style>