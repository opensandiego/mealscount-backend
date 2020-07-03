<template>
    <section class="home">
      <div class="homepage-hero position-relative overflow-hidden" v-bind:style="hero_style">
        <div class="overlay col-md-5 p-lg-5 my-5">
          <h1 class="display-4">Food for Students. Funds for Schools.</h1>
          <hr/>
          <p class="lead">Meals Count is a free tool to help school districts optimize their
            Community Eligibility Provision (CEP) applications, maximize school meal funding, and fight childhood hunger.</p>
           <router-link to="/faq" class="learn btn btn-outline-secondary">Learn More</router-link>
           <router-link to="/explore" class="find filled btn btn-outline-secondary">Find Your District</router-link>
        </div>
      </div>

      <div class="home-cards home-container">
        <div class="centered-background gray" v-bind:style="graybg1"/>
        <div class="centered-background" v-bind:style="greenbg1"/>
        <div class="row">
          <h2 class="col-12 display-5">How Does Meals Count Work?</h2>
          <hr class="fancy-rule"/>
        </div>

        <div class="row d-flex flex-row justify-content-between">
          <div class="card-container p-2">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">LOCATE</h5>
                  <p class="card-text">Select your state and district.</p>
                  <img v-bind:src="icons.locate" alt="Select your state and district" height="180px" />
              </div>
            </div>
          </div>
          <div class="card-container p-2">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">INPUT DATA</h5>
                  <p class="card-text">Input data for the schools in your district</p>
                  <img v-bind:src="icons.inputdata" alt="Input your district's schools and school data" style="margin-top: 30px;" height="150px" />
              </div>
            </div>
          </div>
          <div class="card-container p-2">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">RECOMMENDATIONS</h5>
                  <p class="card-text">Get recommendations on how to group your schools for your CEP Application</p>
                  <img v-bind:src="icons.recommendations" alt="Get recommendations on how to group your schools for your CEP Application" height="150px" />
              </div>
            </div>
          </div>
        </div>

        <div class="why-group row">
          <div class="col-12">
            <router-link class="grouping" to="/faq">Why does grouping matter?</router-link>
          </div>
        </div>
        <div class="get-started row">
          <div class="col-12 text-center">
            <router-link to="/explore" class="btn btn-primary outlined filled">Get Started</router-link>
          </div>
        </div>

      </div>

      <div class="what-is-cep-block home-container">
          <div class="row">
            <h2 class="col-12">What Is CEP?</h2>
          </div>
          <div class="row content-row">
            <div class="col-6">
              <p>
                The Community Eligibility Provision (CEP) is a federally authorized option for schools to serve and receive funding for breakfasts and lunches that are free of charge to all students.
              </p>

              <p>
                CEP helps reduce stigma, prevents student meal debt, and eliminates the need to collect school meal applications. Nourishing students through CEP helps all children learn, grow, and achieve at their fullest potential.  
              <p>
                <router-link to="/faq">Learn more</router-link>
              </p>
            </div>
            <div class="col-6">
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

      <div>
        <div class="newsletter-block home-container text-center">
          <div class="row">
            <h2 class="col-12 display-5">Hear About Updates, Events, and New Features</h2>
          </div>
          <div class="row">
            <div class="col-12 text-center">
              <router-link to="newsletter/" class="btn btn-primary outlined filled">Sign Up For Our Newsletter</router-link>
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
import LOCATE_ICON from '../assets/locate-icon.svg';
import INPUTDATA_ICON from '../assets/inputdata-icon.svg';
import RECOMMENDATIONS_ICON from '../assets/recommendations-icon.svg';
import CENTER_GREEN_BG from '../assets/gradient-swooper.svg';
import CENTER_GRAY_BG from '../assets/center-gray.svg';

export default {
  data() {
    return {
      logos: { cfpa_logo: CFPALogo, 
              openSD_logo: OPENSD,
              hunger_logo: HUNGER
      },
      icons: {
        locate: LOCATE_ICON,
        inputdata: INPUTDATA_ICON,
        recommendations: RECOMMENDATIONS_ICON,
      },
      worker_img: HOMEPAGE_WORKER,
      hero_style: {
        "background-image": "url('"+HOMEPAGE_HERO+"')",
        backgroundSize: 'cover',
      },
      greenbg1: {
        "background-image": "url('"+CENTER_GREEN_BG+"')",
      },
      graybg1: {
        "background-image": "url('"+CENTER_GRAY_BG+"')",
      }

    }
  },
}
</script>



<style scoped lang="scss">

.home-container {
  max-width: 1413px;
  margin: auto;
}

.col-md-5.overlay {
  /*background: rgba(16,16,16,.25);*/
  border-radius: 10px;
  /*width:820px;*/
  /*float:left;*/
}

.centered-background {
    position: absolute;
    top: 900px;
    width: 1930px;
    left: -3px;
    height: 100%;
    background-repeat: no-repeat;
}

.centered-background.gray {
  width: 1499px;
  top: 1567px;
  left: 424px;
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
}

.btn.learn {
  margin-right: 70px;
}
.btn.find {
  margin-right: 0px;
}

.homepage-hero .btn{
  margin-right: 70px;
}
.homepage-hero {
  margin: 0px;
}
.btn.filled {
  background: #F27C3E 0% 0% no-repeat padding-box;
  color: #FFFFFF;
}

.home-cards {
  text-align: center;
  color: black;
  margin: 100px auto;
  
  .card-container {
    display: flex;
    justify-content: center;
  }

  .card {
    height: 442px;
    width: 385px;
    box-shadow: 0px 10px 16px #00000064;
    /* need to pull this from bootstrap */
    @media only screen and (max-width: 1024px) {
      width: 300px;
      height: 500px;
    }
  }
  .card-body {
    margin: auto;
    text-align: center;
    font-size: 24px;
    img {
      position: absolute;
      bottom: 30px;
      left: 120px;
    }
  }
  .card-title {
    margin-top: 39px;
    margin-bottom: 33px;
    font-size: 28px;
    font-weight: bold;
  }
  
  hr {
    border: 3px solid #B0D35C;;
    margin-bottom:  102px;
    width: 120px;
  }

  h2 {
    font-size: 45px;
  }
  .why-group {
    margin-top: 31px;
    font-size: 24px;
    a { color: white; text-decoration: underline; }
  }
  .get-started {
    margin-top: 72px;
    margin-bottom: 207px;
  }
}

.what-is-cep-block {
  h2 {
    text-align: center;
    font-size: 45px; 
    padding-bottom: 24px;
    margin-bottom:  125px;
  }
  .content-row {
    margin: 0px 10px 268px 10px;
    font-size: 31px;
  }
  img {
    width: 100%;
  }
}

.support-block {
  color: black;
  h2 {
    font-size: 45px;
  }
}
.what-is-cep-block {
  color: black;
}
</style>