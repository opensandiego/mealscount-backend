<template>
    <section class="home">
      <div class="homepage-hero position-relative overflow-hidden" v-bind:style="hero_style">
        <div class="overlay col-md-5 p-lg-5 mx-auto my-5">
          <h1 class="display-4">Maximize your CEP funding with Meals Count</h1>
          <hr/>
          <p class="lead">Meals Count is a free tool to help school districts optimize their
            USDA CEP Application, to get more reimbursements for school meals, and help fight child hunger.</p>
           <router-link to="/faq" class="learn btn btn-outline-secondary">Learn More</router-link>
           <router-link to="/explore" class="find btn btn-outline-secondary">Find Your District</router-link>
        </div>
      </div>

      <div class="home-cards home-container">
        <div class="row">
          <h2 class="col-12 display-5">How Does Meals Count Work?</h2>
        </div>

        <div class="row">
          <div class="col-4 card-container">
            <div class="card" style="width: 18rem;">
              <img src="" class="card-img-top" alt="">
              <div class="card-body">
                <h5 class="card-title">LOCATE</h5>
                  <p class="card-text">Select your state and district.</p>
              </div>
            </div>
          </div>
          <div class="card-container col-4">
            <div class="card" style="width: 18rem;">
              <img src="" class="card-img-top" alt="">
              <div class="card-body">
                <h5 class="card-title">INPUT DATA</h5>
                  <p class="card-text">Input your district's schools and school data</p>
              </div>
            </div>
          </div>
          <div class="card-container col-4">
            <div class="card" style="width: 18rem;">
              <img src="" class="card-img-top" alt="">
              <div class="card-body">
                <h5 class="card-title">RECOMMENDATIONS</h5>
                  <p class="card-text">Get recommendations on how to group your schools for your CEP Application</p>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-12">
            <a href="#TODO">Why does grouping matter?</a>
          </div>
        </div>
        <div class="row">
          <div class="col-12 text-center">
            <a href="#TODO" class="btn btn-primary">Get Started</a>
          </div>
        </div>

      </div>

      <div class="what-is-cep-block home-container">
          <div class="row">
            <h2 class="col-12">What Is CEP?</h2>
          </div>
          <div class="row">
            <div class="col-6">
              <p>
                The Community Eligibility Provision (CEP) is a federally authorized option for schools 
                to serve and receive funding for breakfasts and lunches that are free of charge to all students. 
              </p>
              <p>
                It allows the nation’s highest poverty schools and districts to serve breakfast and lunch at 
                no cost to all enrolled students without collecting household applications.
              </p>

              <p>
                <a href="#/faq">Learn more</a>
              </p>
            </div>
            <div class="col=6">
              <img v-bind:src="worker_img" alt="CEP School Lunch"/>
            </div>
          </div>
      </div>

      <div>
        <div class="support-block home-container text-center">
          <div class="row">
            <h2 class="col-12 display-5">Meals Count is developed and supported by</h2>
          </div>
          <div class="row">
            <div class="col-12 text-center">
              <a target="_blank" href="https://opensandiego.org"><img class="logo" v-bind:src="logos.openSD_logo"></a>
              <a target="_blank"  href='https://www.cfpa.net'> <img class='logo' v-bind:src="logos.cfpa_logo" /> </a>     
              <a target="_blank"  href="https://www.sandiegohungercoalition.org/"> <img class="logo" v-bind:src="logos.hunger_logo">  </a>
            </div>
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
import HOMEPAGE_WORKER from '../assets/Image_worker-food.png';

export default {
  data() {
    return {
      logos: { cfpa_logo: CFPALogo, 
              openSD_logo: OPENSD,
              hunger_logo: HUNGER
      },
      worker_img: HOMEPAGE_WORKER,
      hero_style: {
        "background-image": "url('"+HOMEPAGE_HERO+"')",
        backgroundSize: 'cover',
      }
    }
  }
}
</script>



<style scoped lang="scss">
.home-container {
  max-width: 1413px;
  margin: auto;
}
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

.homepage-hero .btn{
  float: left;
}
.homepage-hero {
  margin: 0px;
}
.btn.find {
  background: #F27C3E 0% 0% no-repeat padding-box;
  color: #FFFFFF;
}

.home-cards {
  text-align: center;
  color: black;
  margin: 100px auto;
  .card {
    height: 442px;
    width: 385px;
  }
}

.support-block {
  color: black;
}
.what-is-cep-block {
  color: black;
}

</style>