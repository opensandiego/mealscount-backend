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
            Estimated Annual Reimbursement 
            <sup>1</sup>
          </dt>
            <dd v-if="best_strategy != null">
              {{ (best_strategy.reimbursement * schoolDays) | toUSD }}
              <br />
              ( optimized with {{ best_strategy.name }} strategy )
              <br />
              <a class="btn btn-primary" data-toggle="collapse"h href="#by-group" role="button" aria-expanded="false" aria-controls="by-group">
                By Group
              </a>
              <table class="table collapse" id="by-group">
                <thead>
                  <tr>
                    <th>Group Number</th>
                    <th>Schools</th>
                    <th>Group ISP</th>
                    <th>Est. Reimbursement</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(group,index) in best_strategy.groups" v-bind:key="group.name">
                    <td>Group {{ (index+1) }}</td>
                    <td>{{ group.school_codes.length }} School<span v-if="group.school_codes.length > 1">s</span></td>
                    <td>{{ (group.isp*100).toFixed(1) }}%</td>
                    <td class="text-right">{{ (group.est_reimbursement * schoolDays)|toUSD }}</td>
                  </tr>
                </tbody>
              </table>
            </dd>
            <dd v-else>
              <p>To view reimbursements, please enter in your Average Daily Participation numbers.</p>
            </dd>
          <dt>Determining Rates</dt>
          <div>
            <div>
              <strong>SFA Certified</strong> 
              <p>
                Is your menu certified for the additional 7 cents?              
                <span v-if="editMode"><input v-model="district.sfa_certified" type="checkbox" /></span>
                <span v-else-if="district.sfa_certified">
                  <strong>Yes</strong>
                </span>
                <span v-else>
                  <strong>No</strong>
                </span>
              </p>
            </div>
            <div>
              <strong>NSLA 60%+ Rate</strong>
              <p>
                Were at least 60% of lunches served to students who qualify for free and reduced-price meals in the second preceding school year?
                <span v-if="editMode">
                  <select v-model="district.hhfka_sixty">
                    <option value="less">Less than 60%</option>
                    <option value="more">More than 60%</option>
                    <option value="max">Maximum</option>
                  </select>
                </span>
                <span v-else>
                  <strong v-if="district.hhfka_sixty == 'less'">Less than 60%</strong>
                  <strong v-else-if="district.hhfka_sixty == 'more'">More than 60%</strong>
                  <strong v-else-if="district.hhfka_sixty == 'max'">Maximum Reimbursement</strong>
                </span>
                </p>
            </div>
          </div>
        </dl>
      </div>
</template>

<script>
export default {
    props: ["district","schoolDays","editMode"],
    computed: {
        best_strategy(){
          console.log("computing best strategy for district summary")
          if(this.district.strategies != undefined){
              return this.district.strategies[this.district.best_index];
          }else{
            return null
          }
        }
    }
}
</script>

<style scoped>
#by-group {
  margin-top: 15px;
}
</style>

