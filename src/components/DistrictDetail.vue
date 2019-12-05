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

      <div class="row">
        <dl class="col-sm">
          <dt>State</dt>
          <dd>{{ state_code }}</dd>
          <dt>District Code</dt>
          <dd>{{ district_code}}</dd>
          <dt>District Total Enrolled</dt>
          <dd v-if="district_data != null">{{ district_data.total_enrolled | toCount }}</dd>
          <dt>District-Wide ISP</dt>
          <dd v-if="district_data != null">{{ (district_data.overall_isp*100).toFixed(1) }}%</dd>
          <dt>
            Estimated Annual Reimbursement Range
            <sup>1</sup>
          </dt>
          <dd v-if="best_strategy != null">
            {{ (best_strategy.reimbursement * schoolDays) | toUSD }}
            <br />
            ( optimized with {{ best_strategy.name }} strategy )
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
    </div>
    <div class="row container mx-auto" v-if="district_data != null && viewMode == 'group'">
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
                v-bind:aria-controls="`collapsegroup-${group.id}`"
              >Group {{ group.id }}: {{ group.data.name }}</button>
            </h2>
            <ul>
              <li>Schools: {{ group.schools.length }}</li>
              <li>Group ISP: {{ (group.data.isp*100).toFixed(1) }}%</li>
              <li>Students: {{ group.data.total_eligible | toCount }} Identified Students of {{ group.data.total_enrolled | toCount }} Enrolled</li>
              <li>Daily Meals Served: {{ group.data.daily_breakfast_served }} breakfasts, {{ group.data.daily_lunch_served }} lunches</li>
              <li>Breakfast Reimbursement Rates: {{ district.rates.free_bfast | toUSDx }} / {{ district.rates.paid_bfast | toUSDx }}</li>
              <li>Lunch Reimbursement Rates: {{ district.rates.free_lunch | toUSDx }} / {{ district.rates.paid_lunch | toUSDx }}</li>
              <li>Group Annual Reimbursement Estimate: {{ (group.data.est_reimbursement * schoolDays) | toUSD }} ( {{ group.data.est_reimbursement | toUSD }} per day)</li>
              <li style="color:green" v-if="group.data.cep_eligible">Group CEP Eligible</li>
              <li style="color:red" v-else>Not CEP Eligible</li>
              <li
                style="color:green"
                v-if="group.data.isp >= 0.625"
              >All meals reimbursed at the free rate</li>
              <li
                style="color:green"
                v-if="group.data.isp < 0.625 && group.data.isp >= 0.4"
              >Partial Coverage</li>
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

    <div class="row px-3" v-if="district_data != null && viewMode == 'table'">
      <table class="table col-sm">
        <thead class="thead-dark">
          <tr>
            <td colspan="11">
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
            </td>
          </tr>
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
            <th scope="col">School CEP Eligible</th>
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
            <td>{{ (school.isp >= 0.40)?"✔️":"" }}</td>
          </tr>
        </tbody>
      </table>
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

// TODO "404" if no district?
export default {
  props: ["state_code", "district_code"],
  data() {
    return {
      sort_col: "School Name",
      sort_desc: false,
      school_form: null,
      editMode: false,
      viewMode: "table", // or "group"
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
    edited(){
      return this.district != null && this.district.edited != undefined;
    },
    district_data() {
      if (this.district == null || this.district.data == undefined) {
        return null;
      }
      if(this.district.edited == undefined){
        return this.district.data;
      }
      return this.district.edited;
    },
    grouped_schools() {
      if (this.district == null || this.district_data == null) {
        return [];
      }
      const s = this.district_data.strategies[this.district_data.best_index];
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
      return _.orderBy( grouped, ['data.isp'], 'desc');
    },
    ordered_schools() {
      if (this.district == null || this.district_data == null) {
        return [];
      }
      const schools = this.district_data.schools;
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
      if (this.district == null || this.district_data == null) {
        return null;
      }
      if (!this.district_data.strategies) {
        return null;
      }
      return this.district_data.strategies[this.district_data.best_index];
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
    district(newVal, oldVal) {
      if (this.district != null && this.district_data == null) {
        this.loadDistrictData();
      }
    },
    district_data( newVal, oldVal) {
      if(newVal != null){
        this.init_school_form();
      }

    }
  },
  mounted() {
    if (this.district != null && this.district_data == null) {
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
    init_school_form(){
      console.log("adding schools");
      this.school_form = {};
      this.ordered_schools.forEach(school => {
          this.school_form[school.school_code] = {
            total_enrolled: school.total_enrolled,
            total_eligible: school.total_eligible,
            daily_breakfast_served: school.daily_breakfast_served,
            daily_lunch_served: school.daily_lunch_served,
            active: school.active
          };
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
    },
    submit(){
      console.log("Submitting for optimization",this.school_form) 
      const district_info = {
        schools: this.school_form,
        code: this.district_code,
        name: this.district.name,
        state_code: this.state_code,
      }
      this.$store.dispatch("run_district",district_info);
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