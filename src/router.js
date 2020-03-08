// Routed components
import Home from "./components/Home.vue";
import About from "./components/About.vue";
import CEP from "./components/CEP.vue";
import Contact from "./components/Contact.vue";
import StateDetail from "./components/StateDetail.vue";
import DistrictDetail from "./components/district/DistrictDetail.vue";
import StateMap from "./components/StateMap.vue"
import Faq from "./components/Faq.vue";
import Vue from 'vue';
import VTooltip from 'v-tooltip'
import Router from 'vue-router';
import store from './store.js';
Vue.use(Router, VTooltip)

// Router
export default new Router({
    routes: [
        {
            path: '/', 
            name: 'home',
            component: Home,
        },
        {
            path: '/about', 
            name: 'about',
            component: About,
        },
        {
            path: '/cep', 
            name: 'cep',
            component: CEP,
        },
        {
            path: '/faq', 
            name: 'faq',
            component: Faq,
        },    
        {
            path: '/contact', 
            name: 'contact',
            component: Contact,
        },
        {
            path: '/explore', 
            name: 'map',
            component: StateMap,
            beforeEnter: (to, from, next) => {
                store.dispatch("load_states").then(next)
            } 
        },    
        {
            path: '/explore/:state_code', 
            name: 'state-detail',
            component: StateDetail,
            props: true,
            beforeEnter: (to, from, next) => {
                store.dispatch("load_districts",to.params.state_code).then(next)
            }
        },
        {
            path: '/explore/:state_code/:district_code', 
            name: 'district-detail',
            component: DistrictDetail,
            props: true,
            beforeEnter: (to, from, next) => {
                store.dispatch("load_district",{state:to.params.state_code,code:to.params.district_code}).then(next)
            }
        },
    ]
});