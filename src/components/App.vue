<template>
    <div>
        <nav class="site-header sticky-top py-1">
        <div class="container d-flex flex-column flex-md-row justify-content-between">
          <router-link class="py-2" to="/">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor"
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="d-block mx-auto" role="img"
              viewBox="0 0 24 24" focusable="false">
              <title>Product</title>
              <circle cx="12" cy="12" r="10" />
              <path
                d="M14.31 8l5.74 9.94M9.69 8h11.48M7.38 12l5.74-9.94M9.69 16L3.95 6.06M14.31 16H2.83m13.79-4l-5.74 9.94" />
            </svg>
          </router-link>
          <router-link to="/explore/ca" class="py-2 d-none d-md-inline-block">Explore</router-link>
          <router-link to="/contact" class="py-2 d-none d-md-inline-block">Contact</router-link>
          <router-link to="/about" class="py-2 d-none d-md-inline-block">About</router-link>
        </div>
      </nav>

     <router-view></router-view>
   
      <footer class="container py-5">
        <div class="row">
          <div class="col-12 col-md">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor"
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="d-block mb-2" role="img"
              viewBox="0 0 24 24" focusable="false">
              <title>Product</title>
              <circle cx="12" cy="12" r="10" />
              <path
                d="M14.31 8l5.74 9.94M9.69 8h11.48M7.38 12l5.74-9.94M9.69 16L3.95 6.06M14.31 16H2.83m13.79-4l-5.74 9.94" />
            </svg>
            <small class="d-block mb-3 text-muted">&copy; 2017-2019</small>
          </div>
          <div class="col-6 col-md">
            <h5>Resources</h5>
            <ul class="list-unstyled text-small">
              <li><a class="text-muted" href="https://github.com/opensandiego/mealscount-backend/">MealsCount Source Code</a>
              </li>
              <li><a class="text-muted" href="https://www.fns.usda.gov/school-meals/community-eligibility-provision">USDA CEP Program</a></li>
              <li><a class="text-muted" href="https://www.fns.usda.gov/nslp/community-eligibility-provision-resource-center">USDA CEP Resource Center</a></li>
              <li><a class="text-muted" href="https://github.com/opensandiego/mealscount-backend/blob/validate/CONTRIBUTING.md">MealsCount Contributing Guide</a></li>
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
    this.$store.dispatch("load_districts","ca");
  } 
}
</script>