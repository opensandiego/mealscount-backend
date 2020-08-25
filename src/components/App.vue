<template>
  <div>
    <nav class="navbar navbar-expand-lg d-flex align-items-center">
      <div class="p-2">
        <router-link class="logo" to="/">
          <img v-bind:src="logo" alt="Meals Count" />
        </router-link>
      </div>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarCollapse"
        aria-controls="navbarCollapse"
        aria-expanded="true"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <div class="navbar-nav d-flex justify-content-end">
          <router-link class="nav-item nav-link p-4" to="/explore">Find Your District</router-link>
          <router-link class="nav-item nav-link p-4" to="/faq">FAQ</router-link>
          <router-link class="nav-item nav-link p-4" to="/contact">Contact</router-link>
          <router-link class="nav-item nav-link p-4" to="/about">About</router-link>
          <router-link class="nav-item nav-link p-4" to="/help">Help</router-link>
        </div>
      </div>
    </nav>

    <!--
    <div class="flex-column text-center alert-info py-1">
            CEP Application for 20-21 School Year is now August 31st! <a target="_blank" href="https://www.fns.usda.gov/cn/covid-19-cep-deadlines-waiver">learn more &raquo;</a>
    </div>-->

    <router-view></router-view>

    <footer class="site-footer">
      <div class="nav-container px-3">
        <div class="row py-5">
          <div class="col-6 col-md">
            <h5>Resources</h5>
            <ul class="list-unstyled text-small">
              <li>
                <a
                  href="https://github.com/opensandiego/mealscount-backend/"
                >Meals Count Source Code</a>
              </li>
              <li>
                <a
                  href="https://www.fns.usda.gov/nslp/community-eligibility-provision-resource-center"
                >USDA CEP Resource Center</a>
              </li>
              <li>
                <a
                  href="https://github.com/opensandiego/mealscount-backend/blob/validate/CONTRIBUTING.md"
                >Meals Count Contributing Guide</a>
              </li>
              <li>
                <router-link to="/faq">FAQ</router-link>
              </li>
              <li>
                <router-link to="/help">Help</router-link>
              </li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>Partners</h5>
            <ul class="list-unstyled text-small">
              <li>
                <a href="https://opensandiego.org">Open San Diego</a>
              </li>
              <li>
                <a href="https://www.cfpa.net">CFPA</a>
              </li>
              <li>
                <a href="https://www.sandiegohungercoalition.org/">SD Hunger</a>
              </li>
              <li>
                <a href="https://www.codeforamerica.org/">Code For America</a>
              </li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>Contact</h5>
            <ul class="list-unstyled text-small">
              <li>
                <router-link to="/contact">Contact Us</router-link>
              </li>
              <li>
                <router-link to="/newsletter">Newsletter</router-link>
              </li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>About</h5>
            <ul class="list-unstyled text-small">
              <li>
                <a href="https://github.com/opensandiego/mealscount-backend">Developers</a>
              </li>
              <li>
                <router-link to="/faq">FAQ</router-link>
              </li>
              <li>
                <router-link to="/algorithms">About Algorithms</router-link>
              </li>
            </ul>
          </div>
          <div class="col-12 col-md-4">
            <div class="icon">
              <!--<svg width="134" height="112">
                  <rect width="134" height="112" style="fill:rgb(255,255,255)" />
              </svg>-->
              Meals Count
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script >
import VTooltip from "v-tooltip";
import MealsCountLogo from "../assets/MC_Logo@2x.png";

export default {
  data() {
    return {
      logo: MealsCountLogo
    };
  },
  mounted() {
    this.$store.dispatch("load_states");
    //this.$store.dispatch("load_districts","ca");
  }
};
</script>
