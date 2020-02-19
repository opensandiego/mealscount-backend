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
        set_district_list(state,district_list){
            Vue.set(state.states, district_list.state, district_list.list);
        },
        set_district( state, district ){
            console.log("setting district",district)
            const d = _.filter(state.states[district.state_code], d => d.code == district.code)[0];
            Vue.set(d, 'data', district);
        },
        set_edited_district( state, district ){
            const d = _.filter(state.states[district.state_code], d => d.code == district.code)[0];
            if( d != undefined ){
                Vue.set(d,'edited', district);
            }else{
                console.error("Unabled to locate matching district",district)
            }

        },
    },
    getters: {
        districts: state => {
            // TODO let other states do this
            const state_code = "ca";
            if(state.states[state_code] == undefined){ return [] }
            return state.states[state_code];
        },
        edited_districts: state => {
            return state.edited_districts;
        },
        get_states: state => {
            return state.states;
        },
    },
    actions: {
        load_districts({commit,dispatch}, state_code){
            //const url =`/api/districts/${state_code}/` 
            const url = `/static/${state_code}/districts.json`;
            axios.get(url).then( resp => {
                console.log(`setting ${resp.data.length} districts for ${state_code}`)
                resp.data.forEach( d => d.data = null );
                commit("set_district_list",{state:state_code,list:resp.data});
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
        },
        run_district( {commit,dispatch}, district_info ){
            const url = `/api/districts/optimize/`;
            axios.post(url,district_info).then( resp => {
                const d = resp.data;
                console.log("Updated optimization with",d);
                commit("set_edited_district", d)
            });
        }
    }
})