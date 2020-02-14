// Routed components
import Home from "./components/Home.vue";
import About from "./components/About.vue";
import CEP from "./components/CEP.vue";
import Contact from "./components/Contact.vue";
import StateDetail from "./components/StateDetail.vue";
import DistrictDetail from "./components/DistrictDetail.vue";
import EditDistrict from "./components/EditDistrict.vue";
import Vue from 'vue';
import VTooltip from 'v-tooltip'
import Router from 'vue-router';
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
            path: '/contact', 
            name: 'contact',
            component: Contact,
        },    
        {
            path: '/explore/:state', 
            name: 'state-detail',
            component: StateDetail,
            props: true,
        },
        {
            path: '/explore/:state_code/:district_code', 
            name: 'district-detail',
            component: DistrictDetail,
            props: true,
        },
        {
            path: '/edit-district/', 
            name: 'edit-district',
            component: EditDistrict,
            props: true,
        },
    ]
});