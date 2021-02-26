<template>
    <div class="contact">

        <div v-if="contact.agency">
            <h4>State</h4>
            <p>
                <a target="_blank" :href="contact.agency.cep_website">
                    {{ contact.agency.name }}
                </a>
            </p>
            <p v-for="phone in contact.agency.cep_phone" v-bind:key="phone">
                <a :href="'tel:'+phone">{{ phone }}</a>
            </p>
            <p v-for="email in contact.agency.cep_email" v-bind:key="email">
                <a :href="'mailto:'+email[1]">{{ email[0] }} ( {{ email[1] }} )</a>
            </p>
    </div>

        <div v-if="contact.organizations.length > 0">
            <h4 >Organizations</h4>
            <ul>
                <li v-for="org in contact.organizations" v-bind:key="org.name">
                    <a target="_blank" :href="org.website">
                        {{ org.name }}
                    </a><br>
                    <p v-for="phone in org.phone" v-bind:key="phone">
                        <a :href="'tel:'+phone">{{ phone }}</a>
                    </p>
                    <p v-for="email in org.email" v-bind:key="email">
                        <a :href="'mailto:'+email">{{ email }}</a>
                    </p>
                    <p v-for="phone in org.cep_phone" v-bind:key="phone">
                        CEP Specific: <a :href="'tel:'+phone">{{ phone }}</a>
                    </p>
                    <p v-for="email in org.cep_email" v-bind:key="email">
                        CEP Specific: <a :href="'mailto:'+email">{{ email }}</a>
                    </p>
                </li>
            </ul>
        </div>

        <div v-if="contact.additional" v-html="contact.additional"></div>

    </div>
</template>

<script>
export default {
    props: ["contact"],
}
</script>