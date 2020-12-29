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
        scenarios: [],
    },
    mutations: {
        set_district_list(state, district_list) {
            console.log("Setting district list", district_list,state.states)
            const state_info = state.states[district_list.state];
            state_info.districts = district_list.list
            Vue.set(state.states, district_list.state, state_info);
        },
        set_district(state, district) {
            console.log("setting district", district)
            state.selected_district = district;
            //const d = _.filter(state.states[district.state_code].districts, d => d.code == district.code)[0];
            //Vue.set(d, 'data', district);
        },
        set_edited_district(state, district) {
            state.selected_district = district
        },
        set_states(state, data) {
            state.states = data;
        },
        set_scenarios(state, scenarios) {
            state.scenarios = scenarios;
        },
        add_scenario(state, scenario) {
            state.scenarios.push(scenario)
        },
        remove_scenario(state, i) {
            state.scenarios.splice(i, 1)
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
        get_scenarios: state => {
            return state.scenarios;
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
                }
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
        save_scenario({ state, commit, dispatch }, scenario) {
            commit("add_scenario", scenario)
            dispatch("save_scenarios")
        },
        delete_scenario({ state, commit, dispatch }, i) {
            commit("remove_scenario", i);
            dispatch("save_scenarios")
        },
        save_scenarios({ state }) {
            localStorage.setItem("scenarios", JSON.stringify(state.scenarios));
        },
        load_scenario({ state, commit, dispatch }, i) {
            commit("set_district", state.scenarios[i].district);
        },
        update_scenario_list({ commit, dispatch }) {
            if (localStorage.getItem('scenarios')) {
                try {
                    const scenarios = JSON.parse(localStorage.getItem('scenarios'));
                    commit("set_scenarios", scenarios);
                } catch (e) {
                    console.error("issue loading scenarios", e);
                    localStorage.removeItem("scenarios");
                }
            }
        }
    }
})