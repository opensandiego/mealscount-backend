<template>
    <section class="state-detail">
        <h1>{{ state.name }}</h1>

        <!-- todo v if state is known -->
        <p>TODO Map</p>
        <p>TODO District List</p>
    </section>
</template>

<script>
export default {
    props: ['state_code'] ,
    computed: {
        state() {
            // Todo buld from state_cod
            return {name:"California",code:this.state_code};
        },
        districts(){
            // TODO feed from API? or built-in object?
            return [];
        }
    }
}
</script>