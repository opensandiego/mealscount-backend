<template>
    <div>
        <nav class="site-header sticky-top py-1">
        <div class="container d-flex flex-column flex-md-row justify-content-between">
          <router-link class="py-2" to="/">
            <strong class="icon">
              Meals Count 
              <sup>Beta</sup>
            </strong>
          </router-link>
          <router-link to="/explore" class="py-2 d-none d-md-inline-block">Find Your District</router-link>
          <router-link class="py-2 d-none d-md-inline-block" to="/faq">FAQ </router-link>
          <router-link to="/contact" class="py-2 d-none d-md-inline-block">Contact</router-link>
          <router-link to="/about" class="py-2 d-none d-md-inline-block">About</router-link>
        </div>
        </nav>
    <div class="flex-column text-center alert-info py-1">
            CEP Application for 20-21 School Year is now August 31st! <a target="_blank" href="https://www.fns.usda.gov/cn/covid-19-cep-deadlines-waiver">learn more &raquo;</a>
    </div>

     <router-view></router-view>
   
      <footer class="container py-5">
        <div class="row">
          <div class="col-12 col-md">
            <strong class="icon">
              Meals Count 
              <sup>Beta</sup>
            </strong> 
            <small class="d-block mb-3 text-muted">&copy; 2017-2020</small>
          </div>
          <div class="col-6 col-md">
            <h5>Resources</h5>
            <ul class="list-unstyled text-small">
              <li><a class="text-muted" href="https://github.com/opensandiego/mealscount-backend/">Meals Count Source Code</a>
              </li>
              <li><a class="text-muted" href="https://www.fns.usda.gov/school-meals/community-eligibility-provision">USDA CEP Program</a></li>
              <li><a class="text-muted" href="https://www.fns.usda.gov/nslp/community-eligibility-provision-resource-center">USDA CEP Resource Center</a></li>
              <li><a class="text-muted" href="https://github.com/opensandiego/mealscount-backend/blob/validate/CONTRIBUTING.md">Meals Count Contributing Guide</a></li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>Partners</h5>
            <ul class="list-unstyled text-small">
              <li><a class="text-muted" href="https://opensandiego.org">Open San Diego</a></li>
              <li><a class="text-muted" href="https://www.cfpa.org">CFPA</a></li>
              <li><a class="text-muted" href="https://www.sdhunger.org">SD Hunger</a></li>
              <li><a class="text-muted" href="https://www.codeforamerica.org/">Code For America</a></li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>Contact</h5>
            <ul class="list-unstyled text-small">
              <li><router-link to="/contact" class="text-muted">Contact Us</router-link></li>
              <li><a class="text-muted" href="https://osd-slack-auto-invite.herokuapp.com/">Ask Questions</a></li>
              <li><a class="text-muted" href="https://github.com/opensandiego/mealscount-backend/issues">Post Issues</a></li>
              <li><a class="text-muted" href="https://github.com/opensandiego/mealscount-backend/blob/validate/CONTRIBUTING.md">Contribute</a></li>
              <li><a class="text-muted" href="https://meetup.com/Open-San-Dieog/">Meet In Person</a></li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>About</h5>
            <ul class="list-unstyled text-small">
              <li><a class="text-muted" href="#">Team</a></li>
              <li><a class="text-muted" href="#">Privacy</a></li>
              <li><a class="text-muted" href="https://github.com/opensandiego/mealscount-backend">Developers</a></li>
              <li> <router-link class="text-muted" to="/faq">FAQ </router-link>  </li>
            </ul>
          </div>
        </div>
      </footer>
    </div>
</template>

<script >
import VTooltip from 'v-tooltip';
export default {

  
  
  mounted(){
    this.$store.dispatch("load_states");
    //this.$store.dispatch("load_districts","ca");
  } 
}
</script>
