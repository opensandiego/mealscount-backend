<template>
    <tr
            v-bind:class="{ inactive: !school.active }"
            v-bind:key="school.code"
          >
        <td></td>
        <td>{{ school.school_code }}</td>
        <td>{{ school.school_name }}</td>
        <td>{{ school.school_type }}</td>
        <td>
            <input type="number" v-model="school.total_enrolled" />
        </td>
        <td>
            <input type="number" v-model="school.total_eligible" />
        </td>
        <td>
            <input type="number" v-model="school.daily_breakfast_served" />
        </td>
        <td>
            <input type="number" v-model="school.daily_lunch_served" />
        </td>
        <td>
            <input type="checkbox" v-model="school.active" />
        </td>
        <td>
            {{ ( (school.total_eligible / school.total_enrolled) * 100).toFixed(1) }}%
        </td>
        <td>
            {{  ((school.total_eligible / school.total_enrolled)>=0.4)?"✔️":""  }}
        </td>
        <td><!-- Not Ready {{ (schoolDays * daily_reimbursement_by_school(school.school_code) ) | toUSD }} --> - </td>
    </tr>
</template>

<script>
export default {
    props: ['school']
}
</script>