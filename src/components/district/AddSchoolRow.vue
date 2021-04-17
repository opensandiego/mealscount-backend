<template>
    <tr>
        <td>Add School:</td>
        <td>
            <input placeholder="School Code (required)" v-model="school.school_code" />
        </td>
        <td>
            <input placeholder="School Name" v-model="school.school_name" />
        </td>
        <td>
            <input type="number" v-model.number="school.total_enrolled" min="1" />
        </td>
        <td>
            <input type="number" v-model.number="school.total_eligible" min="0" />
        </td>
        <td>
            <input type="number" v-model.number="school.daily_breakfast_served" min="0" />
        </td>
        <td>
            <input type="number" v-model.number="school.daily_lunch_served" min="0"/>
        </td>
        <td>
            <input type="checkbox" v-model="school.severe_need" />
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
           if( !this.school.school_code ){
                alert("Please enter a school code") 
                return;
           }
           this.$emit("add_school",this.school)
           //this.clear()
        }
    }
}
</script>