<template>
    <tr
            v-bind:class="{ inactive: !school.active, excluded: group == null }"
            v-bind:key="school.code"
            v-bind:style="rowBgStyle"
          >
        <td v-if="group != null">
            <select v-model="school.grouping" @change="$emit('recalculate')">
                <option :value="group">{{ group }} *</option>
                <option v-for="g in group_numbers" :value="g" v-bind:key="g">{{ g }}</option>
            </select>
        </td>
        <td v-else v-tooltip title="Schools marked in group 0 are not included in the grouping calculation" >0</td>
        <td>{{ school.school_code }}</td>
        <td>{{ school.school_name }}</td>
        <td>{{ school.total_enrolled | toCount }}</td>
        <td>{{ school.total_eligible | toCount }}</td>
        <td>{{ school.daily_breakfast_served | toCount }}</td>
        <td>{{ school.daily_lunch_served | toCount }}</td>
        <td>
            <span v-if="school.severe_need">✔️</span>
        </td>
        <td>
            <span v-if="school.active">✔️</span>
        </td>
        <td>
            {{ ( (school.total_eligible / school.total_enrolled) * 100).toFixed(1) }}%
        </td>
        <td>
            {{  ((school.total_eligible / school.total_enrolled)>=0.4)?"✔️":""  }}
        </td> 
        <td class="text-right">
            <span class="school_reimb">{{ reimbursement|toUSD }}</span>
            <div v-if="school.rates != null" class="rate_detail">
                <strong>Site Reimbursement Rates</strong><br>
                Free Breakfast: {{ school.rates.free_bfast | toUSDc }}<br>
                Paid Breakfast: {{ school.rates.paid_bfast | toUSDc }}<br>
                Free Lunch: {{ school.rates.free_lunch | toUSDc }}<br>
                Paid Lunch: {{ school.rates.paid_lunch | toUSDc }}
            </div>
        </td>
    </tr>
</template>

<script>

export default {
    props: ['school','group','color','reimbursement','group_numbers'],
    computed: {
        rowBgStyle(){ 
            return { backgroundColor: this.color };
        }
    },
}
</script>

<style scoped>
    .excluded {
        color: #aaa;
    }
    .rate_detail { display:none; }
    .school_reimb { cursor: pointer; }
    .school_reimb:hover + .rate_detail {
        position: absolute;
        right: 0px;
        background-color: white;
        border: solid 1px black;
        padding: 8px;
        display: block;
    }
</style>
