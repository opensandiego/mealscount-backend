<template>
  <section class="state-detail container my-3" v-if="district != null">
    <div class="row">
      <h1 class="col-sm">{{ district.name }} ({{ district_code }} - {{ state_code }})</h1>
    </div>

    <div class="row">
      <dl class="col-sm">
        <dt>State</dt>
        <dd>{{ state_code }}</dd>
        <dt>District Code</dt>
        <dd>{{ district_code}}</dd>
        <dt>Total Enrolled</dt>
        <dd>{{ district.total_enrolled.toLocaleString() }}</dd>
        <dt>Overall ISP</dt>
        <dd>{{ (district.overall_isp*100).toFixed(1) }}%</dd>
        <dt>
          Estimated Annual Reimbursement Range
          <sup>1</sup>
        </dt>
        <dd v-if="best_strategy != null">
          <strong>Winning Strategy:</strong>
          {{ best_strategy.name }}
          <br />
          <strong>High:</strong>
          ${{ Math.round(best_strategy.reimbursement.high_end_estimate * 180).toLocaleString({ style: 'currency', currency: 'USD' }) }}
          <br />
          <strong>Low:</strong>
          ${{ Math.round(best_strategy.reimbursement.low_end_estimate * 180).toLocaleString({ style: 'currency', currency: 'USD' }) }}
          <br />
          <sup>1</sup>Based on 180 days in school year
        </dd>
      </dl>
    </div>

    <div class="row" v-if="district.data != null">
      <table class="table col-sm">
        <thead class="thead-dark">
          <tr>
            <th scope="col" @click="set_sort('grouping')">Recommended Grouping</th>
            <th scope="col" @click="set_sort('school_code')">School Code</th>
            <th scope="col" @click="set_sort('school_name')">School Name</th>
            <th scope="col">School Type</th>
            <th scope="col" @click="set_sort('total_enrolled')">Total Enrolled</th>
            <th scope="col">Total Eligible</th>
            <th scope="col">Daily Breakfast Served</th>
            <th scope="col">Daily Lunch Served</th>
            <th scope="col" @click="set_sort('active')">Included in Optimization</th>
            <th scope="col" @click="set_sort('isp')">Overall ISP</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-bind:class="{ inactive: !school.active }"
            v-if="school_form != null"
            v-for="school in ordered_schools"
            v-bind:key="school.code"
          >
            <td>{{ (best_group_index!=null?best_group_index[school.school_code]:'n/a') }}</td>
            <td>{{ school.school_code }}</td>
            <td>{{ school.school_name }}</td>
            <td>{{ school.school_type }}</td>
            <td v-if="editMode">
              <input type="number" v-model="school_form[school.school_code].total_enrolled" />
            </td>
            <td v-else>{{ school.total_enrolled.toLocaleString() }}</td>
            <td v-if="editMode">
              <input type="number" v-model="school_form[school.school_code].total_eligible" />
            </td>
            <td v-else>{{ school.total_eligible.toLocaleString() }}</td>
            <td v-if="editMode">
              <input type="number" v-model="school_form[school.school_code].daily_breakfast_served" />
            </td>
            <td v-else>{{ school.daily_breakfast_served.toLocaleString() }}</td>
            <td v-if="editMode">
              <input type="number" v-model="school_form[school.school_code].daily_lunch_served" />
            </td>
            <td v-else>{{ school.daily_lunch_served.toLocaleString() }}</td>
            <td v-if="editMode">
              <input type="checkbox" v-model="school_form[school.school_code].active" />
            </td>
            <td v-else><span v-if="school.active">✔️</span></td>
            <td>{{ (school.isp * 100).toFixed(1) }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div>
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
        v-on:click="toggleEdit"
      >cancel</button>
    </div>
  </section>
</template>

<script>
import * as _ from "lodash";

// TODO "404" if no district?
export default {
  props: ["state_code", "district_code"],
  data() {
    return {
      sort_col: "School Name",
      sort_desc: false,
      school_form: null,
      editMode: false,
    };
  },
  computed: {
    district() {
      var districts = _.filter(
        this.$store.getters.districts,
        d => d.code == this.district_code
      );
      if (districts.length) {
        return districts[0];
      }
      return null;
    },
    ordered_schools() {
      if (this.district == null || this.district.data == undefined) {
        return [];
      }
      const schools = this.district.data.schools;
      schools.forEach(s => {
        s.grouping = this.best_group_index[s.school_code];
      });
      return _.orderBy(
        schools,
        [this.sort_col],
        [this.sort_desc ? "desc" : "asc"]
      );
    },
    best_strategy() {
      if (this.district == null || this.district.data == null) {
        return null;
      }
      if (!this.district.data.strategies) {
        return null;
      }
      return this.district.data.strategies[this.district.data.best_index];
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
    ordered_schools(newVal, oldVal) {
      if (this.school_form == null && newVal != null && newVal.length > 0) {
        console.log("adding schools");
        this.school_form = {};
        newVal.forEach(school => {
          this.school_form[school.school_code] = {
            total_enrolled: school.total_enrolled,
            total_eligible: school.total_eligible,
            daily_breakfast_served: school.daily_breakfast_served,
            daily_lunch_served: school.daily_lunch_served,
            active: school.active
          };
        });
      }
    },
    district(newVal, oldVal) {
      if (this.district != null && this.district.data == null) {
        this.loadDistrictData();
      }
    }
  },
  mounted() {
    if (this.district != null && this.district.data == null) {
      this.loadDistrictData();
    }
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
    toggleEdit() {
        this.editMode = !this.editMode;
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