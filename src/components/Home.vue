<template>
  <section class="home">
    <div class="hero-container">
      <div class="slider">
        <figure>
          <img v-bind:src="heros.girldesk" alt="girl sitting at a desk" />
          <img v-bind:src="heros.hero1" alt="food" />
          <img v-bind:src="heros.kidseating" alt="kids eating" />
          <img v-bind:src="heros.hero2" alt="food zoomed-in" />
        </figure>
      </div>
      <div class="homepage-hero overflow-hidden" v-bind:style="hero_style">
        <div class="home-shadow">
          <div class="overlay col-md-7 col-xl-6 p-lg-4 my-5 mx-lg-5 ">
            <h1 class="display-4">
              Food for Students. <span>Funds for Schools.</span>
            </h1>
            <hr />
            <p class="lead">
              Meals Count is a free tool to help school districts optimize their
              Community Eligibility Provision (CEP) applications, maximize
              school meal funding, and fight childhood hunger.
            </p>
            <router-link
              to="/explore"
              class="find filled btn btn-outline-secondary"
              >Find Your District</router-link
            >
            <router-link to="/faq" class="learn btn btn-outline-secondary"
              >Learn More</router-link
            >
          </div>
        </div>
      </div>
    </div>

    <div class="centered-background gray" v-bind:style="graybg1" />
    <div class="centered-background" v-bind:style="greenbg1" />
    <div class="home-cards home-container">
      <div class="row">
        <h2 class="col-12 display-5">How Does Meals Count Work?</h2>
        <hr class="fancy-rule" />
      </div>

      <div class="cards-container">
        <div class="card-container p-2">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">LOCATE</h5>
              <p class="card-text">Select your state and district.</p>
              <img
                v-bind:src="icons.locate"
                alt="Select your state and district"
                height="180px"
              />
            </div>
          </div>
        </div>
        <div class="card-container p-2">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">INPUT DATA</h5>
              <p class="card-text">
                Input your district's schools and school data
              </p>
              <img
                v-bind:src="icons.inputdata"
                alt="Input your district's schools and school data"
                style="margin-top: 30px; padding-left: 10px;"
                height="103px"
              />
            </div>
          </div>
        </div>
        <div class="card-container p-2">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">RECOMMENDATIONS</h5>
              <p class="card-text">
                Get recommendations on how to group your schools for your CEP
                Application
              </p>
              <img
                v-bind:src="icons.recommendations"
                alt="Get recommendations on how to group your schools for your CEP Application"
                height="103px"
                style="padding-left: 10px;"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="why-group row">
        <div class="col-12">
          <router-link class="grouping" to="/faq"
            >Why does grouping matter?</router-link
          >
        </div>
      </div>
      <div class="get-started row">
        <div class="col-12 text-center">
          <router-link to="/explore" class="btn btn-primary outlined filled"
            >Get Started</router-link
          >
        </div>
      </div>
    </div>

    <div class="what-is-cep-block home-container">
      <div class="row">
        <h2 class="col-12">What Is CEP?</h2>
        <hr class="fancy-rule" />
      </div>
      <div class="row content-row">
        <div class="col-12 col-md-6 ">
          <p>
            The Community Eligibility Provision (CEP) is a federally authorized
            option for schools to serve and receive funding for breakfasts and
            lunches that are free of charge to all students.
          </p>

          <p>
            CEP helps reduce stigma, prevents student meal debt, and eliminates
            the need to collect school meal applications. Nourishing students
            through CEP helps all children learn, grow, and achieve at their
            fullest potential.
          </p>

          <p>
            <router-link to="/faq" style="text-decoration: underline;"
              >Learn more</router-link
            >
          </p>
        </div>
        <div class="col-12 col-md-6">
          <img v-bind:src="worker_img" alt="CEP School Lunch" />
        </div>
      </div>
    </div>

    <div>
      <div class="support-block home-container text-center">
        <div class="row">
          <h2 class="col-12 display-5">
            Meals Count is developed and supported by
          </h2>
        </div>
        <div class="row">
          <div class="col-12 text-center">
            <a target="_blank" href="https://opensandiego.org"
              ><img class="logo" v-bind:src="logos.openSD_logo"
            /></a>
            <a target="_blank" href="https://www.cfpa.net">
              <img class="logo" v-bind:src="logos.cfpa_logo" />
            </a>
            <a target="_blank" href="https://www.sandiegohungercoalition.org/">
              <img class="logo" v-bind:src="logos.hunger_logo" />
            </a>
          </div>
        </div>
      </div>
    </div>

    <div class="newsletter-block home-container text-center">
      <div class="row">
        <h2 class="col-12 display-5">
          Hear About Updates, Events, and New Features
        </h2>
      </div>
      <div class="row">
        <div class="col-12 text-center">
          <router-link to="newsletter/" class="btn btn-primary outlined filled"
            >Sign Up For Our Newsletter</router-link
          >
        </div>
      </div>
    </div>
    <!-- 
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
      </div> -->
  </section>
</template>

<script>
import CFPALogo from "../assets/cfpalogo.png";
import OPENSD from "../assets/openSD.jpeg";
import HUNGER from "../assets/hunger.jpg";
import HOMEPAGE_HERO from "../assets/homepage_hero.jpg";
import HOMEPAGE_WORKER from "../assets/Image_worker-food.png";
import LOCATE_ICON from "../assets/locate-icon.svg";
import INPUTDATA_ICON from "../assets/inputdata-icon.svg";
import RECOMMENDATIONS_ICON from "../assets/recommendations-icon.svg";
import CENTER_GREEN_BG from "../assets/green-diagonal-background.png";
import CENTER_GRAY_BG from "../assets/center-gray.svg";
import HERO_GIRL_DESK from "../assets/Hero_girl-desk.png";
import HERO_KIDS_EATING from "../assets/Hero_kids-eating.png";
import HOMEPAGE_HERO2 from "../assets/homepage_hero2.jpg";

export default {
  data() {
    return {
      logos: { cfpa_logo: CFPALogo, openSD_logo: OPENSD, hunger_logo: HUNGER },
      icons: {
        locate: LOCATE_ICON,
        inputdata: INPUTDATA_ICON,
        recommendations: RECOMMENDATIONS_ICON,
      },
      worker_img: HOMEPAGE_WORKER,
      heros: {
        hero1: HOMEPAGE_HERO,
        hero2: HOMEPAGE_HERO2,
        girldesk: HERO_GIRL_DESK,
        kidseating: HERO_KIDS_EATING,
      },
      // Moved to scss
      //hero_style: {
      //  "background-image":
      //    "linear-gradient(90deg, rgb(0, 0, 0, .5) 0%, rgba(31, 31, 31, 0.2) 70%, rgba(84, 84, 84, 0) 100%)",
      //  backgroundSize: "cover",
      //},
      greenbg1: {
        "background-image": "url('" + CENTER_GREEN_BG + "')",
      },
      graybg1: {
        "background-image": "url('" + CENTER_GRAY_BG + "')",
      },
    };
  },
  // From: https://forum.vuejs.org/t/how-do-i-add-remove-classes-to-body/1219/12
  // .. not my favorite method, but need to fix home layout issue
  methods: {
    toggleBodyClass(addRemoveClass, className) {
      const el = document.body;

      if (addRemoveClass === "addClass") {
        el.classList.add(className);
      } else {
        el.classList.remove(className);
      }
    },
  },
  mounted() {
    this.toggleBodyClass("addClass", "body-home");
  },
  destroyed() {
    this.toggleBodyClass("removeClass", "body-home");
  },
};
</script>

<style scoped lang="scss">
.hero-container {
  position: relative;
}
@keyframes slider {
  0% {
    left: 0;
  }
  30% {
    left: 0;
  }
  35% {
    left: -100%;
  }
  65% {
    left: -100%;
  }
  70% {
    left: -200%;
  }
  95% {
    left: -200%;
  }
  100% {
    left: -300%;
  }
}

.slider {
  display: none;
  @media only screen and (min-width: 1370px) {
    overflow: hidden;
    display: block;
  }
}

.homepage-hero,
.slider {
  @media only screen and (min-width: 1370px) {
    height: 515px;
  }
  @media only screen and (min-width: 1600px) {
    height: 590px;
  }
}

.slider figure img {
  width: 25%;
  float: left;
}

.slider figure {
  @media only screen and (min-width: 1370px) {
    position: relative;
    width: 400%;
    margin: 0;
    left: 0;
    animation: 15s slider forwards;
    animation-iteration-count: 1;
  }
}
.home {
  position: relative;
  overflow: hidden;
}
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
  //top: px;
  width: 1930px;
  left: -3px;
  height: 100%;
  background-repeat: no-repeat;
  @media only screen and (min-width: 500px) {
    top: 505px;
  }
  @media only screen and (min-width: 1600px) {
    top: 600px;
  }
}

.centered-background.gray {
  width: 1499px;
  top: 1122px;
  left: 424px;
  @media only screen and (min-width: 1600px) {
    top: 1175px;
  }
}

section {
  //color: white;
  text-align: left;
}

p.lead,
h1 {
  text-align: left;
  font-weight: bold;
  font-size: 40px;
  color: white;
  font-family: "century-gothic";
}

h1 span {
  display: block;
}

p.lead {
  font-size: 22px;
  font-weight: bold;
  clear: left;
  margin-bottom: 38px;
  padding-top: 23px;
}

div.active-development.alert {
  display: none;
}

hr {
  display: block;
  float: left;
  border-top: 4px solid white;
  width: 109px;
}

.btn {
  background: #ffffff 0% 0% no-repeat padding-box;
  border: 3px solid #f27c3e;
  border-radius: 31px;
  text-align: center;
  font: Bold 17px/34px century-gothic;
  letter-spacing: 0.02px;
  color: #f27c3e;
  opacity: 1;
  width: 200px;
}

.btn.learn {
  margin-right: 0px;
  &:hover {
    color: #ffffff;
    background: #f27c3e;
  }
}
.btn.find {
  margin-right: 55px;
}

.homepage-hero .btn {
  @media only screen and (max-width: 1000px) {
    display: block;
    margin: 20px auto;
    //width: 210px;
    /*font: Bold 20px/38px century-gothic;*/
  }
}

.home-shadow {
  max-width: 1600px;
  margin: auto;
}

.homepage-hero {
  margin: 0px;
  z-index: 1;
  top: 0;
  position: relative;
  background-image: linear-gradient(
      90deg,
      rgba(0, 0, 0, 0.5) 0%,
      rgba(31, 31, 31, 0.2) 70%,
      rgba(84, 84, 84, 0) 100%
    ),
    url("../assets/homepage_hero2.jpg");
  background-size: cover;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: auto;

  @media only screen and (min-width: 1370px) {
    //height: 570px;
    position: absolute;
    background-image: linear-gradient(
      90deg,
      rgba(0, 0, 0, 0.5) 0%,
      rgba(31, 31, 31, 0.2) 70%,
      rgba(84, 84, 84, 0) 100%
    );
  }
  @media only screen and (min-width: 1600px) {
    //height: 700px;
    padding: 40px;
  }
}
.btn.filled {
  background: #f27c3e 0% 0% no-repeat padding-box;
  color: #ffffff;
  &:hover {
    color: #f27c3e;
    background: #ffffff;
  }
}
.fancy-rule {
  border: 3px solid #b0d35c;
  margin-bottom: 70px;
  width: 120px;
}

.home-cards {
  text-align: center;
  color: black;
  margin: 120px auto;
  padding: 0 15px;

  .cards-container {
    @media only screen and (min-width: 1000px) {
      display: flex;
      justify-content: space-evenly;
    }
    @media only screen and (min-width: 1600px) {
      justify-content: space-between;
      width: 1200px;
      margin: auto;
    }
  }

  .card-container {
    display: flex;
    justify-content: center;
  }

  .card {

    width: 300px;
    height: 400px;
    box-shadow: 0px 10px 16px #00000064;
    /* need to pull this from bootstrap */
    //@media only screen and (max-width: 1600px) {
    //  width: 300px;
    //  height: 400px;
    //}
  }
  .card-body {
    margin: auto;
    text-align: center;
    font-size: 20px;
    img {
      position: absolute;
      bottom: 50px;
      left: 86px;
    }
    p {
      padding: 0 15px;
    }
    /*@media only screen and (max-width: 1600px) {
      font-size: 20px;
      img {
        left: 85px;
        bottom: 50px;
      }
      p {
        padding: 0 15px;
      }
    } */
  }
  .card-title {
    margin-top: 17px;
    margin-bottom: 30px;
    font-size: 22px;
    //font-size: 28px;
    font-weight: bold;
    /*@media only screen and (max-width: 1600px) {
      font-size: 22px;
    }*/
  }

  h2 {
    font-size: 32px;
    @media only screen and (min-width: 1600px) {
      //font-size: 45px;
    }
  }
  .why-group {
    margin-top: 31px;
    text-decoration: underline;
    font-size: 20px;
    @media only screen and (min-width: 1600px) {
      //font-size: 24px;
    }
    @media only screen and (min-width: 1000px) {
      a {
        color: white;
      }
    }
  }
  .get-started {
    margin-top: 72px;
    //margin-bottom: 207px;
  }
}

.what-is-cep-block {
  h2 {
    text-align: center;
    font-size: 32px;
    @media only screen and (min-width: 1600px) {
      //font-size: 45px;
    }
  }
  .content-row {
    margin: 8px auto 120px auto;
    //font-size: 31px;
    font-size: 22px;
    //width: 100%;
    @media only screen and (min-width: 1060px) {
      width: 1050px;
      & > div {
        padding-right: 40px;
      }
    }

    @media only screen and (min-width: 1600px) {
      //width: 1350px;
    }
    @media only screen and (max-width: 1600px) {
      //font-size: 22px;
    }
  }
  img {
    width: 100%;
  }
}

.support-block {
  color: black;
  margin-bottom: 100px;
  padding: 0 15px;
  h2 {
    font-size: 32px;
    margin-bottom: 50px;
    @media only screen and (min-width: 1600px) {
      //font-size: 45px;
    }
  }
}
.what-is-cep-block {
  color: black;
  @media only screen and (min-width: 1200px) {
    display: flex;
    flex-direction: column;
    /* justify-content: center; */
    align-items: center;
  }
}

.newsletter-block {
  padding: 0 15px;
  h2 {
    margin-bottom: 70px;
    @media only screen and (min-width: 1600px) {
      //font-size: 45px;
    }
  }
}
</style>
