<template>
    <tr
            v-bind:class="{ inactive: !school.active, excluded: group == null }"
            v-bind:key="school.code"
            v-bind:style="rowBgStyle"
          >
        <td v-if="group != null">{{ group }}</td>
        <td v-else v-tooltip title="Schools marked in group 0 are not included in the grouping calculation" >0</td>
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
        <td>
            {{ ( (school.total_eligible / school.total_enrolled) * 100).toFixed(1) }}%
        </td>
        <td>
            {{  ((school.total_eligible / school.total_enrolled)>=0.4)?"✔️":""  }}
        </td> 
        <td> {{ reimbursement|toUSD }}</td>
    </tr>
</template>

<script>

export default {
    props: ['school','group','color','reimbursement'],
    computed: {
        rowBgStyle(){ 
            return { backgroundColor: this.color };
        }
    }
}
</script>

<style scoped>
    .excluded {
        color: #aaa;
    }
</style>
