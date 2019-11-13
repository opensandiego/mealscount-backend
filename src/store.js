import axios from "axios"
import * as _ from "lodash"
import Vue from "vue";
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        states: {'ca':[]},
    },
    mutations: {
        set_district_list(state,districts){
            state.states['ca'] = districts;
        },
        set_district( state, district ){
            console.log("setting district",district)
            const d = _.filter(state.states[district.state_code], d => d.code == district.code)[0];
            d.data = district;
        }
    },
    getters: {
        districts: state => {
            const state_code = "ca";
            if(state.states[state_code] == undefined){ return [] }
            return state.states[state_code];
        }
    },
    actions: {
        load_districts({commit,dispatch}, state_code){
            //const url =`/api/districts/${state_code}/` 
            const url = `/static/${state_code}/districts.json`;
            axios.get(url).then( resp => {
                console.log(`setting ${resp.data.length} districts for ${state_code}`)
                resp.data.forEach( d => d.data = null );
                commit("set_district_list",resp.data);
            })
        },
        load_district( {commit,dispatch}, district ){
            const url = `/static/${district.state}/${district.code}_district.json`
            console.log("loading district data from ",url)
            axios.get(url).then( resp => {
                const d = resp.data
                d.state_code = district.state
                commit("set_district",d);
            })
        }
    }
})