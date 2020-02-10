<template>
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
        <td v-if="editMode">
            {{ ( (school_form[school.school_code].total_eligible / school_form[school.school_code].total_enrolled) * 100).toFixed(1) }}%
        </td>
        <td v-else>{{ (school.isp * 100).toFixed(1) }}%</td>
        <td v-if="editMode">
            {{  ((school_form[school.school_code].total_eligible / school_form[school.school_code].total_enrolled)>=0.4)?"✔️":""  }}%
        </td>
        <td>{{ (school.isp >= 0.40)?"✔️":"" }}</td>
        </tr>
        <tr v-if="editMode == true" class="add_row">
        <td>Add School:</td>
        <td><input type="text" v-model="new_school_to_add.code" name="school_code" placeholder="School Code" /></td>
        <td><input type="text" v-model="new_school_to_add.name" name="school_name" placeholder="School Name" /></td>
        <td><input type="text" v-model="new_school_to_add.type" name="school_type" value="Public" /></td>
        <td colspan="7"><button v-on:click="add_school" class="btn btn-primary">Add</button></td>
        </tr>
</template>

<script>
export default {
    props: ['school_data']
}
</script>