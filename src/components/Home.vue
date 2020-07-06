<template>
    <section class="home">
      <div class="homepage-hero position-relative overflow-hidden" v-bind:style="hero_style">
        <div class="home-shadow">
        <div class="overlay col-md-5 p-lg-5 my-5">
          <h1 class="display-4">Maximize your CEP funding with Meals Count</h1>
          <hr/>
          <p class="lead">Meals Count is a free tool to help school districts optimize their
            USDA CEP Application, to get more reimbursements for school meals, and help fight child hunger.</p>
           <router-link to="/faq" class="learn btn btn-outline-secondary">Learn More</router-link>
           <router-link to="/explore" class="find filled btn btn-outline-secondary">Find Your District</router-link>
        </div>
        </div>
      </div>

      <div class="home-cards home-container">
        <div class="centered-background gray" v-bind:style="graybg1"/>
        <div class="centered-background" v-bind:style="greenbg1"/>
        <div class="row">
          <h2 class="col-12 display-5">How Does Meals Count Work?</h2>
          <hr class="fancy-rule"/>
        </div>

        <div class="cards-container">
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
                  <p class="card-text">Input your district's schools and school data</p>
                  <img v-bind:src="icons.inputdata" alt="Input your district's schools and school data" style="margin-top: 30px;" height="103px" />
              </div>
            </div>
          </div>
          <div class="card-container p-2">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">RECOMMENDATIONS</h5>
                  <p class="card-text">Get recommendations on how to group your schools for your CEP Application</p>
                  <img v-bind:src="icons.recommendations" alt="Get recommendations on how to group your schools for your CEP Application" height="103px" />
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
            <hr class="fancy-rule"/>
          </div>
          <div class="row content-row">
            <div class="col-12 col-md-6 pb-4">
              <p>
                The Community Eligibility Provision (CEP) is a federally authorized option for schools 
                to serve and receive funding for breakfasts and lunches that are free of charge to all students. 
              </p>
              <p>
                It allows the nation’s highest poverty schools and districts to serve breakfast and lunch at 
                no cost to all enrolled students without collecting household applications.
              </p>

              <p>
                <router-link to="/faq">Learn more</router-link>
              </p>
            </div>
            <div class="col-12 col-md-6">
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
        "background-image": "linear-gradient(90deg, rgb(0, 0, 0, .5) 0%, rgba(31, 31, 31, 0.2) 70%, rgba(84, 84, 84, 0) 100%), url('"+HOMEPAGE_HERO+"')",
        backgroundSize: 'cover',
      },
      greenbg1: {
        "background-image": "url('"+CENTER_GREEN_BG+"')",
      },
      graybg1: {
        "background-image": "url('"+CENTER_GRAY_BG+"')",
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

.col-md-5.overlay {
  /*background: rgba(16,16,16,.25);*/
  border-radius: 10px;
  /*width:820px;*/
  /*float:left;*/
}

/*.col-md-5 {
  @media (max-width: 700px) {
    max-width: 55%;
  }
}*/

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
  padding-top: 25px;
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
  font: Bold 22px/40px century-gothic;
  letter-spacing: 0.02px;
  color: #F27C3E;
  opacity: 1;
  width: 260px;
  height: 75;

}

.btn.learn {
  margin-right: 70px;
  &:hover {
    color: #FFFFFF;
    background: #F27C3E;
  }
}
.btn.find {
  margin-right: 0px;
}

.homepage-hero .btn{

  @media only screen and (max-width: 1600px) {
    display: block;
    margin: 20px auto;
    width: 240px;
    /*font: Bold 20px/38px century-gothic;*/
  }
}
.homepage-hero {
  margin: 0px;
}
.btn.filled {
  background: #F27C3E 0% 0% no-repeat padding-box;
  color: #FFFFFF;
      &:hover {
    color: #F27C3E;
    background: #FFFFFF;
  }
}
.fancy-rule {
  border: 3px solid #B0D35C;;
  margin-bottom:  102px;
  width: 120px;
}

.home-cards {
  text-align: center;
  color: black;
  margin: 100px auto;

  .cards-container {
    @media only screen and (min-width: 1000px){
      display: flex;
      justify-content: space-between;
    }
  }

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
      height:430px;
    }
  }
  .card-body {
    margin: auto;
    text-align: center;
    font-size: 24px;
    img {
      position: absolute;
      bottom: 70px;
      left: 135px;
    }
    @media only screen and (max-width: 1024px) {
      font-size: 20px;
      img {
        left: 95px;
        bottom:55px;
      }
    }
  }
  .card-title {
    margin-top: 39px;
    margin-bottom: 33px;
    font-size: 28px;
    font-weight: bold;
    @media only screen and (max-width: 1024px) {
      font-size: 25px;
    }
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
  }
  .content-row {
    margin: 0px 10px 268px 10px;
    font-size: 31px;
    @media only screen and (max-width: 1000px){
      font-size: 25px;
    }
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