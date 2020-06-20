<template>
    <section class="home">
      <div class="homepage-hero position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center bg-light" v-bind:style="hero_style">
        <div class="overlay col-md-5 p-lg-5 mx-auto my-5">
          <h1 class="display-4">Maximize your CEP funding with Meals Count</h1>
          <hr/>
          <p class="lead">Meals Count is a free tool to help school districts optimize their
            USDA CEP Application, to get more reimbursements for school meals, and help fight child hunger.</p>
            <div class="active-development alert alert-primary">Meals Count is under active development, and may change. If you have any feedback, comments or questions, please <router-link to="/contact">contact us</router-link></div>
           <router-link to="/faq" class="learn btn btn-outline-secondary">Learn More</router-link>
           <router-link to="/explore" class="find btn btn-outline-secondary">Find Your District</router-link>
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
import HOMEPAGE_HERO from '../assets/homepage_hero2.jpg';

export default {
  data() {
    return {
      logos: { cfpa_logo: CFPALogo, 
              openSD_logo: OPENSD,
              hunger_logo: HUNGER
      },
      hero_style: {
        "background-image": "url('"+HOMEPAGE_HERO+"')",
        backgroundSize: 'cover',
      }
    }
  }
}
</script>



<style scoped>
.overlay {
  /*background: rgba(16,16,16,.25);*/
  border-radius: 10px;
  width:820px;
  float:left;
}

section {
  color: white;
  text-align: left;
}

p.lead, h1 {
    text-align: left;
    font-weight: bold;
    font-size: 55px;
    color: white;
    font-family: "century-gothic";
}

p.lead {
  font-size: 24px;
  font-weight: bold;
  clear: left;
  margin-bottom: 70px;
}

div.active-development.alert {
  display: none;
}

hr {
  display: block;
  float: left;
  border-top: 5px solid white;
  width: 120px;
}

.btn {
  float: left;
  background: #FFFFFF 0% 0% no-repeat padding-box;
  border: 3px solid #F27C3E;
  border-radius: 31px;
  text-align: center;
  font: Bold 22px/50px century-gothic;
  letter-spacing: 0.02px;
  color: #F27C3E;
  opacity: 1;
  width: 250px;
  height: 75;
  margin-right: 70px;
}

.btn.find {
  background: #F27C3E 0% 0% no-repeat padding-box;
  color: #FFFFFF;
}


</style>