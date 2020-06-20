<template>
  <div>
    <div class="nav-container site-header d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3">
      <h5 class="my-0 mr-md-auto font-weight-normal">
          <router-link class="logo" to="/">
            <img v-bind:src="logo" alt="Meals Count" />
          </router-link>
      </h5>
      <nav>
          <router-link to="/explore">Find Your District</router-link>
          <router-link to="/faq">FAQ </router-link>
          <router-link to="/contact">Contact</router-link>
          <router-link to="/about">About</router-link>
      </nav>
    </div>

        <!--
    <div class="flex-column text-center alert-info py-1">
            CEP Application for 20-21 School Year is now August 31st! <a target="_blank" href="https://www.fns.usda.gov/cn/covid-19-cep-deadlines-waiver">learn more &raquo;</a>
    </div>-->

     <router-view></router-view>
   
      <footer class="site-footer">
        <div class="nav-container px-3">
          <div class="row py-5">
            <div class="col-2">
              <h5>Resources</h5>
              <ul class="list-unstyled text-small">
                <li><a  href="https://github.com/opensandiego/mealscount-backend/">Meals Count Source Code</a>
                </li>
                <li><a  href="https://www.fns.usda.gov/school-meals/community-eligibility-provision">USDA CEP Program</a></li>
                <li><a  href="https://www.fns.usda.gov/nslp/community-eligibility-provision-resource-center">USDA CEP Resource Center</a></li>
                <li><a  href="https://github.com/opensandiego/mealscount-backend/blob/validate/CONTRIBUTING.md">Meals Count Contributing Guide</a></li>
              </ul>
            </div>
            <div class="col-2">
              <h5>Partners</h5>
              <ul class="list-unstyled text-small">
                <li><a  href="https://opensandiego.org">Open San Diego</a></li>
                <li><a  href="https://www.cfpa.org">CFPA</a></li>
                <li><a  href="https://www.sdhunger.org">SD Hunger</a></li>
                <li><a  href="https://www.codeforamerica.org/">Code For America</a></li>
              </ul>
            </div>
            <div class="col-2">
              <h5>Contact</h5>
              <ul class="list-unstyled text-small">
                <li><router-link to="/contact" >Contact Us</router-link></li>
                <li><a  href="https://osd-slack-auto-invite.herokuapp.com/">Ask Questions</a></li>
                <li><a  href="https://github.com/opensandiego/mealscount-backend/issues">Post Issues</a></li>
                <li><a  href="https://github.com/opensandiego/mealscount-backend/blob/validate/CONTRIBUTING.md">Contribute</a></li>
                <li><a  href="https://meetup.com/Open-San-Dieog/">Meet In Person</a></li>
              </ul>
            </div>
            <div class="col-2">
              <h5>About</h5>
              <ul class="list-unstyled text-small">
                <li><a  href="#">Team</a></li>
                <li><a  href="#">Privacy</a></li>
                <li><a  href="https://github.com/opensandiego/mealscount-backend">Developers</a></li>
                <li> <router-link  to="/faq">FAQ </router-link>  </li>
              </ul>
            </div>
            <div class="col-4">
              <div class="icon">
                <svg width="134" height="112">
                  <rect width="134" height="112" style="fill:rgb(255,255,255)" />
                </svg>
                eals Count
              </div> 
            </div>
          </div>
        </div>
      </footer>
    </div>
</template>

<script >
import VTooltip from 'v-tooltip';
import MealsCountLogo from '../assets/MC_Logo@2x.png';

export default {
  data(){
    return {
      logo: MealsCountLogo,
    }
  },
  mounted(){
    this.$store.dispatch("load_states");
    //this.$store.dispatch("load_districts","ca");
  } 
}
</script>
