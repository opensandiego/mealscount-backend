import axios from "axios"
import * as _ from "lodash"
import Vue from "vue";
import Vuex from 'vuex';

Vue.use(Vuex);

const TIMEOUT = 60 * 10 // 10 Minute Timeout
const DEFAULT_RATES = { "free_lunch": 3.31, "paid_lunch": 0.31, "free_bfast": 2.14, "paid_bfast": 0.31 }

export default new Vuex.Store({
    state: {
        states: {},
        selected_district: null,
        history: [],
        district_data: {},
    },
    mutations: {
        set_district_list(state, district_list) {
            console.log("Setting district list", district_list,state.states)
            const state_info = state.states[district_list.state];
            state_info.districts = district_list.list
            Vue.set(state.states, district_list.state, state_info);
        },
        set_district(state, district) {
            // These are the "raw" districts loaded from the server
            // if we have saved data for the district raw data, then prefill that now
            if( state.district_data  && 
                state.district_data[district.state_code] != undefined && 
                state.district_data[district.state_code][district.code] != undefined){ 
                    const d = state.district_data[district.state_code][district.code]
                    district.schools.forEach( s => {
                        if( d[s.school_code] != undefined ){
                            const s1 = d[s.school_code]
                            s.total_enrolled = s1.total_enrolled
                            s.total_eligible = s1.total_eligible
                            s.daily_breakfast_served = s1.daily_breakfast_served
                            s.daily_lunch_served = s1.daily_lunch_served
                        }
                    })
                // load school numbers
            }
            state.selected_district = district;
        },
        set_edited_district(state, district) {
            // These have been edited. We want to preserve our history here
            // rcord history
            district.revision = state.history.length + 1
            district.revised_at = new Date()
            state.history.push( district )

            // update district_data for this district
            if( state.district_data[district.state_code] == undefined){
                state.district_data[district.state_code] = {}
            }
            const d = {}
            district.schools.forEach( s => {
                d[s.school_code] = {
                    total_enrolled:s.total_enrolled, 
                    total_eligible: s.total_eligible, 
                    daily_breakfast_served: s.daily_breakfast_served,
                    daily_lunch_served: s.daily_lunch_served,
                }
            })
            console.log("preserving district data",district.state_code,district.code,d)
            state.district_data[district.state_code][district.code]  = d

            state.selected_district = district
        },
        set_states(state, data) {
            state.states = data;
        },
        set_district_data(state,district_data){
            state.district_data = district_data;
        },
        clear_district_data(state, district){
            if(state.district_data[district.state_code] == undefined){ return }
            delete state.district_data[district.state_code][district.code]
        }
    },
    getters: {
        edited_districts: state => {
            return state.edited_districts;
        },
        get_states: state => {
            return state.states;
        },
        get_state: (state) => (code) => {
            return state.states[code];
        },
        selected_district: state => {
            return state.selected_district;
        },
        get_history: (state) => (state_code,district_code) => {
            return state.history.filter( d => d.code == district_code && d.state_code == state_code )
        },
    },
    actions: {
        load_states({ state, commit, dispatch }) {
            if(Object.keys(state.states).length != 0){
                return
            }
            const url = `/api/states/`;
            axios.get(url).then(resp => {
                for (var k in resp.data) {
                    resp.data[k].districts = null;
                }
                commit('set_states', resp.data);
            })
        },
        load_districts({ commit, dispatch }, state_code) {
            //const url =`/api/districts/${state_code}/` 
            const url = `/static/${state_code}/districts.json`;
            axios.get(url).then(resp => {
                console.log(`setting ${resp.data.length} districts for ${state_code}`)
                resp.data.forEach(d => d.data = null);
                commit("set_district_list", { state: state_code, list: resp.data });
            })
        },
        load_district({ commit, dispatch }, district) {
            const url = `/static/${district.state}/${district.code}_district.json`
            console.log("loading district data from ", url)
            axios.get(url).then(resp => {
                const d = resp.data
                d.state_code = district.state
                commit("set_district", d);
            })
        },
        new_district({ commit, dispatch }, state_code) {
            const d = {
                state_code: state_code,
                code: 'new',
                schools: [],
                rates: DEFAULT_RATES,
                best_index: 0,
                strategies: [{ name: "n/a", groups: [] }],
                name: "Untitled District",
            }
            commit("set_district", d)
        },
        run_district({ commit, dispatch }, district) {
            // TODO make the async option triggered explicitely from index.html data- tag
            const url = `/api/districts/optimize-async/`; 
            axios.post(url, district).then(resp => {
                const d = resp.data;
                if (resp.data.results_url != undefined) {
                    setTimeout(t => {
                        dispatch("poll_for_results", { url: d.results_url, count: TIMEOUT })
                    }, 1000);
                }else{
                    // If not async
                    console.log("Updated optimization with",d);
                    commit("set_edited_district", d)
                    dispatch('save_district_data')
                }
            });
        },
        calculate_district({ commit, dispatch }, district) {
            const url = `/api/districts/calculate/`; 
            axios.post(url, district).then(resp => {
                const d = resp.data;
                console.log("Calculated district to",d);
                commit("set_edited_district", d)
                dispatch('save_district_data')
            });
        },
        poll_for_results({ commit, dispatch }, target) {
            axios.get(target.url).then(resp => {
                console.log("results received at ", target.url);
                commit("set_edited_district", resp.data);
            }).catch(error => {
                const resp = error.response;
                console.log(resp, target.count)
                if (resp.status == 403 && target.count > 0) {
                    console.log("polling for results at ", target.url);
                    setTimeout(t => {
                        dispatch("poll_for_results", { url: target.url, count: target.count - 1 })
                    }, 1000);
                } else {
                    alert("Error retrieving results, please try again");
                }
            })
        },
        save_district_data({ state,commit }) {                
            localStorage.setItem("district_data", JSON.stringify(state.district_data));
        },
        load_district_data({ commit, dispatch }) {
            if (localStorage.getItem('district_data')) {
                try {
                    const district_data = JSON.parse(localStorage.getItem('district_data'));
                    commit("set_district_data", district_data);
                } catch (e) {
                    console.error("issue loading district_data", e);
                    localStorage.removeItem("district_data");
                }
            }
        },
        clear_district_data( {commit,dispatch}, district) {
            commit("clear_district_data",district ) 
            dispatch("save_district_data")
        },
        load_district_revision( {state,commit }, district_revision){
            const revisions = state.history.filter( d => d.revision == district_revision)
            if( revisions.length == 0){ alert("Unable to find Revision " + district_revision)}
            commit("set_district", revisions[0])
        }
    }
})