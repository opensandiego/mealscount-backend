import './style.scss';
import 'bootstrap';
import Vue from 'vue';

// Core application bits
import App from './components/App.vue'
import store from './store.js';
import router from './router.js';
import { toUSD, toCount, toUSDx, toUSDc } from './filters.js';
import { VTooltip, VPopover, VClosePopover } from 'v-tooltip'

import VueGtag from "vue-gtag";

const body = document.getElementsByTagName("body")[0]

if(body.dataset.analyticsId){
    Vue.use(VueGtag, {
        config: { id: body.dataset.analyticsId }
    }, router ); 
    console.log("tracking analytics to ",body.dataset.analyticsId)
}

 
// Register global filters
Vue.filter('toUSD', toUSD);
Vue.filter('toUSDx', toUSDx);
Vue.filter('toUSDc', toUSDc );
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
