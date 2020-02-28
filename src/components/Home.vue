<template>
    <section>
      <div class="homepage-hero position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center bg-light" v-bind:style="hero_style">
        <div class="col-md-5 p-lg-5 mx-auto my-5">
          <h1 class="display-4 font-weight-normal">Maximize your CEP Funding with <strong>Meals Count</strong></h1>
          <p class="lead font-weight-normal">MealsCount is an Open Source, Free tool to help school districts optimize their
            USDA CEP Application, to get more reimbursements for school meals, and help fight child hunger.</p>
          <a class="btn btn-outline-secondary" href="#">Learn More</a>
        </div>
      </div>

      <div class="d-md-flex flex-md-equal w-100 my-md-3 pl-md-3">
        <div class="bg-dark mr-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden">
          <div class="my-3 py-3">
            <h2 class="display-5">What Is CEP?</h2>
            <p class="lead">The Community Eligibility Provision (CEP) is a USDA program that provides funding for free
              school meals based upon the school's eligible population.</p>
          </div>
        </div>
        <div class="bg-light mr-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden">
          <div class="my-3 p-3">
            <h2 class="display-5">Meals Count is developed and supported by</h2>
            <br>
            <a target="_blank" href="https://opensandiego.org"><img class="logo" v-bind:src="logos.openSD_logo"></a>
            <a target="_blank"  href='https://www.cfpa.net'> <img class='logo' v-bind:src="logos.cfpa_logo" /> </a>     
            <a target="_blank"  href="https://www.sandiegohungercoalition.org/"> <img class="logo" v-bind:src="logos.hunger_logo">  </a>
            
          </div>
        </div>
      </div>

      <div class="d-md-flex flex-md-equal w-100 my-md-3 pl-md-3">
        <div class="bg-light mr-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden">
          <div class="my-3 p-3">
            <h2 class="display-5">How Does Meals Count Work?</h2>
            <p class="lead">Districts can submit their schools to the USDA to get reimbursed for school meals. Reimbursement
              is based on the ISP eligibility of the schools.</p>
          </div>
        </div>
      </div>
    </section>
</template>


<script>
import CFPALogo from '../assets/cfpalogo.png';
import OPENSD from '../assets/openSD.jpeg';
import HUNGER from '../assets/hunger.jpg';
import HOMEPAGE_HERO from '../assets/homepage_hero.jpg';

export default {
  data() {
    return {
     logos: { cfpa_logo: CFPALogo, 
              openSD_logo: OPENSD,
              hunger_logo: HUNGER
                },
      hero_style: {
        /*"background-image": "url('"+HOMEPAGE_HERO+"')",*/
        backgroundSize: 'cover',
      }
    }
  }
}
</script>

