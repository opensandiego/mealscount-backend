import './style.scss';
import 'bootstrap';
import Vue from 'vue';

// Core application bits
import App from './components/App.vue'
import store from './store.js';
import router from './router.js';
import { toUSD, toCount, toUSDx } from './filters.js';
import { VTooltip, VPopover, VClosePopover } from 'v-tooltip'

 
// Register global filters
Vue.filter('toUSD', toUSD);
Vue.filter('toUSDx', toUSDx);
Vue.filter('toCount', toCount );

Vue.use(VTooltip)

Vue.directive('tooltip', VTooltip)

// App
new Vue({
    el: '#app',
    store,
    router,
    VTooltip,
    render: h => h(App)
})
