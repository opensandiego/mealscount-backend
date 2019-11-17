import './style.scss';
import 'bootstrap';
import Vue from 'vue';

// Core application bits
import App from './components/App.vue'
import store from './store.js';
import router from './router.js';
import { toUSD, toCount } from './filters.js';


// Register global filters
Vue.filter('toUSD', toUSD);
Vue.filter('toCount', toCount );

// App
new Vue({
    el: '#app',
    store,
    router,
    render: h => h(App)
})
