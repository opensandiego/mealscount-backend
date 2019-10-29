import axios from "axios"
import * as _ from "lodash"
import Vue from "vue";
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        districts: null,
    },
    mutations: {
        set_districts(state,districts){
            state.districts = districts;
        }
    },
    getters: {
        districts: state => {
            return state.districts;
        }
    },
    actions: {
        load_districts({commit,dispatch}, state_code){
            axios.get(`/api/districts/${state_code}/`).then( resp => {
                console.log(`setting ${resp.data.length} districts for ${state_code}`)
                commit("set_districts",resp.data);
            })
        }
    }
})