<template>
  <div>
    <div class="flex-column text-center alert-warning py-1 small">
          <!--<strong>Reminder</strong> - Download your data <strong>BEFORE April 1st 2021</strong>! All student data must be current as of <strong>April 1</strong> of the year prior to implementing the CEP. -->
          <!--<a target="_blank" href="https://www.fns.usda.gov/cn/covid-19-cep-deadlines-waiver">learn more &raquo;</a>-->
          <strong>Updated</strong> - CEP Deadlines Have Been Extended, make sure you download your data by June 30th! <router-link to="/faq">Learn More</router-link>!
    </div>

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
          <router-link class="nav-item nav-link p-4" to="/explore"
            >Find Your District</router-link
          >
          <router-link class="nav-item nav-link p-4" to="/faq">FAQ</router-link>
          <router-link class="nav-item nav-link p-4" to="/contact"
            >Contact</router-link
          >
          <router-link class="nav-item nav-link p-4" to="/about"
            >About</router-link
          >
          <router-link class="nav-item nav-link p-4" to="/help"
            >Help</router-link
          >
        </div>
      </div>
    </nav>

    <router-view></router-view>

    <footer class="site-footer">
      <div class="bottom-background gray" v-bind:style="footGrey" />
      <div class="bottom-background" v-bind:style="footGreen" />
      <div class="nav-container">
        <div class="row pt-5">
          <div class="col-6 col-md">
            <h5>Resources</h5>
            <ul class="list-unstyled text-small">
              <li>
                <a href="https://github.com/opensandiego/mealscount-backend/"
                  >Meals Count Source Code</a
                >
              </li>
              <li>
                <a
                  href="https://www.fns.usda.gov/nslp/community-eligibility-provision-resource-center"
                  >USDA CEP Resource Center</a
                >
              </li>
              <li>
                <a
                  href="https://github.com/opensandiego/mealscount-backend/blob/validate/CONTRIBUTING.md"
                  >Meals Count Contributing Guide</a
                >
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
                <a href="https://www.nourishca.org">Nourish California</a>
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
                <a href="https://github.com/opensandiego/mealscount-backend"
                  >Developers</a
                >
              </li>
              <li>
                <router-link to="/faq">FAQ</router-link>
              </li>
              <li>
                <router-link to="/algorithms">About Algorithms</router-link>
              </li>
              <li>
                <router-link to="/integrating-with-excel">Integrating With Microsoft Excel</router-link>
              </li>
            </ul>
          </div>
          <div class="col-12 col-md-4">
            <div class="icon">
              <!--<svg width="134" height="112">
                  <rect width="134" height="112" style="fill:rgb(255,255,255)" />
              </svg>-->
              <div class="M">
                <div class="footerM" v-bind:style="footerM" />
              </div>
              <p>eals Count</p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import VTooltip from "v-tooltip";
import MealsCountLogo from "../assets/MC_Logo@2x.png";
import FOOTERM from "../assets/Union_2.svg";
import FOOTERGREY from "../assets/grey-angle-two.svg";
import FOOTERGREEN from "../assets/green-angle.svg";

export default {
  data() {
    return {
      logo: MealsCountLogo,
      footerM: {
        "background-image": "url('" + FOOTERM + "')",
      },
      footGrey: {
        "background-image": "url('" + FOOTERGREY + "')",
      },
      footGreen: {
        "background-image": "url('" + FOOTERGREEN + "')",
      },
    };
  },
  mounted() {
    this.$store.dispatch("load_states");
    //this.$store.dispatch("load_districts","ca");
  },
};
</script>

<style scoped lang="scss">
.M {
  width: 105px;
  height: 90px;
  position: relative;

  @media only screen and (min-width: 1400px) {
    margin-left: 80px;
  }
  @media only screen and (min-width: 1600px) {
    width: 136px;
    height: 120px;
  }
}
.footerM {
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-size: 130px;
  @media only screen and (max-width: 1600px) {
    background-size: 100px;
  }
}
.icon p {
  padding-top: 38px;
  position: absolute;
  left: 105px;

  @media only screen and (min-width: 1400px) {
    left: 185px;
  }
  @media only screen and (min-width: 1600px) {
    left: 212px;
    top: 71px;
  }
}
.bottom-background {
  position: absolute;
  width: 1930px;
  height: 100%;
  background-repeat: no-repeat;
  visibility: hidden;
  @media only screen and (min-width: 1400px) {
    visibility: visible;
  }
}
</style>
