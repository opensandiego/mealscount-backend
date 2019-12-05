<template>
  <section class="state-detail my-3" v-if="district != null">
    <div class="container">
      <div class="row">
        <h1 class="col-sm">Edit {{ district.name }} ({{ district_code }} - {{ state_code }})</h1>
      </div>

      <div class="row">
        <dl class="col-sm">
          <dt>State</dt>
          <dd>{{ state_code }}</dd>
          <dt>District Code</dt>
          <dd>{{ district_code}}</dd>
          <dt>District Total Enrolled</dt>
          <dd>{{ district.total_enrolled | toCount }}</dd>
          <dt>District-Wide ISP</dt>
          <dd>{{ (district.overall_isp*100).toFixed(1) }}%</dd>
          <dt>
            Estimated Annual Reimbursement Range
            <sup>1</sup>
          </dt>
          <dd v-if="best_strategy != null">
            {{ (best_strategy.reimbursement * schoolDays) | toUSD }}
            <br>( optimized with {{ best_strategy.name }} strategy )
            <br />
          </dd>
        </dl>
      </div>
    </div> 

    <div class="row px-3" v-if="district.data != null && viewMode == 'table'">
      <table class="table col-sm">
        <thead class="thead-dark">
          <tr>
            <th scope="col" @click="set_sort('grouping')">Recommended Grouping</th>
            <th scope="col" @click="set_sort('school_code')">School Code</th>
            <th scope="col" @click="set_sort('school_name')">School Name</th>
            <th scope="col">School Type</th>
            <th scope="col" @click="set_sort('total_enrolled')">Total Enrolled</th>
            <th scope="col">
              Total Eligible
              <sup>2</sup>
            </th>
            <th scope="col">
              Daily Breakfast Served
              <sup>3</sup>
            </th>
            <th scope="col">
              Daily Lunch Served
              <sup>3</sup>
            </th>
            <th scope="col" @click="set_sort('active')">Included in Optimization</th>
            <th scope="col" @click="set_sort('isp')">School ISP</th>
            <th scope="col">CEP Eligible</th>
          </tr>
        </thead>
        <tbody v-if="school_form != null">
          <tr
            v-bind:class="{ inactive: !school.active }"
            v-for="school in ordered_schools"
            v-bind:key="school.code"
          >
            <td>{{ (best_group_index!=null?best_group_index[school.school_code]:'n/a') }}</td>
            <td>{{ school.school_code }}</td>
            <td>{{ school.school_name }}</td>
            <td>{{ school.school_type }}</td>
            <td>
              <input type="number" v-model="school_form[school.school_code].total_enrolled" />
            </td>
            <td>
              <input type="number" v-model="school_form[school.school_code].total_eligible" />
            </td>
            <td>
              <input type="number" v-model="school_form[school.school_code].daily_breakfast_served" />
            </td>
            <td>
              <input type="number" v-model="school_form[school.school_code].daily_lunch_served" />
            </td>
            <td>
              <input type="checkbox" v-model="school_form[school.school_code].active" />
            </td>
            <td>{{ (school.isp * 100).toFixed(1) }}%</td>
            <td>{{ (school.isp >= 0.40)?"✔️":"" }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </section>
</template>

<script>
import * as _ from "lodash";

export default {
  props: ["state_code", "district_code"],
  data() {
    return {
      sort_col: "School Name",
      sort_desc: false,
      school_form: [],
      editMode: false,
      viewMode: "group", // or "table"
      schoolDays: 180,
    };
  },
  computed: {
  },
  watch: {
  },
  methods: {
    loadDistrictData() {
      this.$store.dispatch("load_district", {
        code: this.district_code,
        state: this.state_code
      });
    },
    set_sort(col) {
      if (col == this.sort_col) {
        this.sort_desc = !this.sort_desc;
      } else {
        this.sort_col = col;
        this.sort_desc = false;
      }
    },
    submit(){
      this.$store.dispatch("run_district",this.school_form);
    }
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
</style>