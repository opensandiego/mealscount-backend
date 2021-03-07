<template>
 <section class="container mt-5" v-if="state">
    <router-link :to="{name:'faq'}">&laquo; Back to FAQ</router-link>

    <h1 class="headline text-center mb-4">Meals Count FAQ - {{ state.name }}</h1>


    <div class="faq" v-html="state.faq"></div>

    <div class="card" v-if="state.contact">
        <div class="card-header">
            <h2 id="contact">Contact Information for {{ state.name }}</h2>
        </div>
        <div class="card-body">
            <ContactDisplay v-if="state.contact"  v-bind:contact="state.contact" />
        </div>
    </div>

    <div class="district-link center m-4 text-center">
        <router-link class="btn btn-primary" :to="{name:'state-detail', params: {state_code:state_code} }" >
            View Districts in {{ state.name }}
        </router-link>
    </div>

 </section>
</template>


<script>
import ContactDisplay from "./ContactDisplay.vue";

export default {
    components:{ContactDisplay},
    props: ["state_code"],
    computed: {
        state() {
            return this.$store.getters.get_state(this.state_code);
        }
    },
}
</script>

<style scoped>

.district_link {
    margin: 10px auto;
    text-align: center;
}
h3 {
  margin-top: 40px;
}

</style>

