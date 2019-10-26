// Routed components
import Home from "./components/Home.vue";
import About from "./components/About.vue";
import CEP from "./components/CEP.vue";
import Contact from "./components/Contact.vue";
import StateDetail from "./components/StateDetail.vue";
import Vue from 'vue';
import Router from 'vue-router';
Vue.use(Router)

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
            name: 'state-detaill',
            component: StateDetail,
            props: true,
        },
    ]
});