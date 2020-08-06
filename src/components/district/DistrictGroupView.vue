<template>
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
                    <th v-tooltip title="Placeholder!" scope="col">
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
</template>

<script>
export default {
    props: ['grouped_schools','district'],
    data(){
        return {
            sort_col: null,
        }
    } ,
    methods: {
        set_sort(key){

        }
    }
}
</script>