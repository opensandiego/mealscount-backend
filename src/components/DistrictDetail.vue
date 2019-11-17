<template>
  <section class="state-detail container my-3" v-if="district != null">
    <div class="row">
      <div class="container">
        <router-link :to="{name:'state-detail', params: {state:state_code} }">&laquo; Back to state</router-link>
      </div>
    </div>

    <div class="row">
      <h1 class="col-sm">{{ district.name }} ({{ district_code }} - {{ state_code }})</h1>
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
          <strong>Winning Strategy:</strong>
          {{ best_strategy.name }}
          <br />
          <strong>High:</strong>
          {{ (best_strategy.reimbursement.high_end_estimate * schoolDays) | toUSD }}
          <br />
          <strong>Low:</strong>
          {{ (best_strategy.reimbursement.low_end_estimate * schoolDays) | toUSD }}
          <br />
        </dd>
      </dl>
    </div>

    <div class="row">
        <div class="col-sm mb-3">
            View By 
            <select v-model="viewMode">
                <option value="group">Group</option>
                <option value="table">All Schools</option>
            </select>
        </div>
    </div>

    <div class="row" v-if="district.data != null && viewMode == 'group'">
      <div class="col-sm accordion" id="groupedDisplay">
        <div v-for="group in grouped_schools" class="card" v-bind:key="group.id">
          <div class="card-header" v-bind:id="`card-${group.id}`">
            <h2 class="mb-0">
              <button
                class="btn btn-link collapsed"
                type="button"
                data-toggle="collapse"
                v-bind:data-target="`#collapsegroup-${group.id}`"
                aria-expanded="false"
                v-bind:aria-controls="`collapsegroup-${group.id}`">
                Group {{ group.id }}: {{ group.data.name }}</button>
            </h2>
            <ul>
                <li>Schools: {{ group.schools.length }}</li>
                <li>Group ISP: {{ (group.data.isp*100).toFixed(1) }}%</li>
                <li>Group Total Enrolled: {{ group.data.total_enrolled | toCount }}</li>
                <li>Covered Students: {{ group.data.covered_students | toCount }}</li>
                <li>Group Total Eligible: {{ group.data.total_eligible | toCount }}</li>
                <li>Group Reimbursement Estimate: {{ (group.data.est_reimbursement.low * schoolDays) | toUSD }} - {{ (group.data.est_reimbursement.high * schoolDays ) | toUSD }}</li>
                <li style="color:green" v-if="group.data.cep_eligible">CEP Eligible</li>
                <li style="color:red" v-else>Not CEP Eligible</li>
            </ul>
          </div>

          <div
            v-bind:id="`collapsegroup-${group.id}`"
            class="collapse"
            v-bind:aria-labelledby="`card-${group.id}`"
            data-parent="#groupedDisplay"
          >
            <div class="card-body">
              <table class="table col-sm">
                <thead class="thead-dark">
                  <tr>
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
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="school in group.schools"
                    v-bind:class="{ inactive: !school.active }"
                    v-bind:key="school.code"
                  >
                    <td>{{ school.school_code }}</td>
                    <td>{{ school.school_name }}</td>
                    <td>{{ school.school_type }}</td>
                    <td>{{ school.total_enrolled | toCount }}</td>
                    <td>{{ school.total_eligible | toCount }}</td>
                    <td>{{ school.daily_breakfast_served | toCount }}</td>
                    <td>{{ school.daily_lunch_served | toCount }}</td>
                    <td>
                      <span v-if="school.active">✔️</span>
                    </td>
                    <td>{{ (school.isp * 100).toFixed(1) }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row" v-if="district.data != null && viewMode == 'table'">
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
            <td v-if="editMode">
              <input type="number" v-model="school_form[school.school_code].total_enrolled" />
            </td>
            <td v-else>{{ school.total_enrolled | toCount }}</td>
            <td v-if="editMode">
              <input type="number" v-model="school_form[school.school_code].total_eligible" />
            </td>
            <td v-else>{{ school.total_eligible | toCount }}</td>
            <td v-if="editMode">
              <input type="number" v-model="school_form[school.school_code].daily_breakfast_served" />
            </td>
            <td v-else>{{ school.daily_breakfast_served | toCount }}</td>
            <td v-if="editMode">
              <input type="number" v-model="school_form[school.school_code].daily_lunch_served" />
            </td>
            <td v-else>{{ school.daily_lunch_served | toCount }}</td>
            <td v-if="editMode">
              <input type="checkbox" v-model="school_form[school.school_code].active" />
            </td>
            <td v-else>
              <span v-if="school.active">✔️</span>
            </td>
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
    <div>
      <sup>1</sup>Based on {{ schoolDays }} days in school year
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

// TODO "404" if no district?
export default {
  props: ["state_code", "district_code"],
  data() {
    return {
      sort_col: "School Name",
      sort_desc: false,
      school_form: null,
      editMode: false,
      viewMode: "group", // or "table"
      schoolDays: 180,
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
    grouped_schools() {
      if (this.district == null || this.district.data == undefined) {
        return [];
      }
      const s = this.district.data.strategies[this.district.data.best_index];
      const grouped = [];
      const schools = this.ordered_schools;
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
      return grouped;
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