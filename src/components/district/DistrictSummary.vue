<template>
      <div class="row">
        <dl class="col-sm">
          <dt>State</dt>
          <dd>{{ district.state_code }}</dd>
          <dt>District Code</dt>
          <dd>{{ district.code}}</dd>
          <dt>District Total Enrolled</dt>
          <dd v-if="district != null">{{ district.total_enrolled | toCount }}</dd>
          <dt>District-Wide ISP</dt>
          <dd v-if="district != null">{{ (district.overall_isp*100).toFixed(1) }}%</dd>
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
          <dt>Federal Reimbursement Rates</dt>
          <dd>
            <ul v-if="district.rates">
              <li>Lunch (free) <span v-if="editMode"><input v-model.number="district.rates.free_lunch" ></span><span v-else>{{ district.rates.free_lunch | toUSDx }}</span>  </li>
              <li>Lunch (paid) <span v-if="editMode"><input v-model.number="district.rates.paid_lunch" ></span><span v-else>{{ district.rates.paid_lunch | toUSDx }}</span>  </li>
              <li>Breakfast (free)  <span v-if="editMode"><input v-model.number="district.rates.free_bfast" ></span><span v-else>{{ district.rates.free_bfast | toUSDx }}</span>  </li>
              <li>Breakfast (paid)  <span v-if="editMode"><input v-model.number="district.rates.paid_bfast" ></span><span v-else>{{ district.rates.paid_bfast | toUSDx }}</span>  </li>
            </ul>
          </dd>
        </dl>
      </div>
</template>

<script>
export default {
    props: ["district","schoolDays","editMode"],
    computed: {
        best_strategy(){
            return this.district.strategies[this.district.best_index];
        }
    }
}
</script>