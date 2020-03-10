<template>
    <tr>
        <td>Add School:</td>
        <td>
            <input placeholder="School Code" v-model="school.school_code" />
        </td>
        <td>
            <input placeholder="School Name" v-model="school.school_name" />
        </td>
        <td>
            <select v-model="school.school_type">
                <option value="Public">Public</option>
                <option value="Charter">Public</option>
                <option value="Other">Public</option>
            </select>
        </td>
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
        <td>
            <button
                class="btn btn-primary"
                @click="add"
            >Add School</button>
        </td>
    </tr>
</template>

<script>
export default {
    data() {
        return {
            school: {
                school_code: "",
                school_name: "",
                school_type: "Public",
                total_enrolled: 100,
                total_eligible: 50,
                daily_breakfast_served: 25, 
                daily_lunch_served: 50,
                active: true,
            }
        }
    },
    methods: {
        clear(){
            // important that we instantiate a new object, 
            // otherwise we will clear the row we just added!
            this.school = {
                school_code: "",
                school_name: "",
                school_type: "Public",
                total_enrolled: 100,
                total_eligible: 50,
                daily_breakfast_served: 25, 
                daily_lunch_served: 50,
                active: true,
            }
        },
        add(){
            // TODO validate we have everything we need
           this.$emit("add_school",this.school)
           this.clear()
        }
    }
}
</script>