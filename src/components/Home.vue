<template>
  <section class="home">
    <div
      class="homepage-hero position-relative overflow-hidden"
      v-bind:style="hero_style"
    >
      <div class="home-shadow">
        <div class="overlay col-md-7 col-xl-6 p-lg-5 my-5 mx-lg-5 ">
          <h1 class="display-4">Food for Students. Funds for Schools.</h1>
          <hr />
          <p class="lead">
            Meals Count is a free tool to help school districts optimize their
            Community Eligibility Provision (CEP) applications, maximize school
            meal funding, and fight childhood hunger.
          </p>
          <router-link to="/faq" class="learn btn btn-outline-secondary"
            >Learn More</router-link
          >
          <router-link
            to="/explore"
            class="find filled btn btn-outline-secondary"
            >Find Your District</router-link
          >
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
            <router-link to="/faq">Learn more</router-link>
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

    <div>
      <div class="newsletter-block home-container text-center">
        <div class="row">
          <h2 class="col-12 display-5">
            Hear About Updates, Events, and New Features
          </h2>
        </div>
        <div class="row">
          <div class="col-12 text-center">
            <router-link
              to="newsletter/"
              class="btn btn-primary outlined filled"
              >Sign Up For Our Newsletter</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import CFPALogo from "../assets/cfpalogo.png";
import OPENSD from "../assets/openSD.jpeg";
import HUNGER from "../assets/hunger.jpg";
import HOMEPAGE_HERO from "../assets/homepage_hero2.jpg";
import HOMEPAGE_WORKER from "../assets/Image_worker-food.png";
import LOCATE_ICON from "../assets/locate-icon.svg";
import INPUTDATA_ICON from "../assets/inputdata-icon.svg";
import RECOMMENDATIONS_ICON from "../assets/recommendations-icon.svg";
import CENTER_GREEN_BG from "../assets/gradient-swooper.svg";
import CENTER_GRAY_BG from "../assets/center-gray.svg";

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
      hero_style: {
        "background-image":
          "linear-gradient(90deg, rgb(0, 0, 0, .5) 0%, rgba(31, 31, 31, 0.2) 70%, rgba(84, 84, 84, 0) 100%), url('" +
          HOMEPAGE_HERO +
          "')",
        backgroundSize: "cover",
      },
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
  top: 550px;
  width: 1930px;
  left: -3px;
  height: 100%;
  background-repeat: no-repeat;
  @media only screen and (min-width: 1600px) {
    top: 800px;
  }
}

.centered-background.gray {
  width: 1499px;
  top: 1217px;
  left: 424px;
  @media only screen and (min-width: 1600px) {
    top: 1467px;
  }
}

section {
  color: white;
  text-align: left;
}

p.lead,
h1 {
  text-align: left;
  font-weight: bold;
  font-size: 42px;
  color: white;
  font-family: "century-gothic";
  @media only screen and (min-width: 1600px) {
    font: normal normal bold 55px/65px Century Gothic;
  }
}

p.lead {
  font-size: 20px;
  font-weight: bold;
  clear: left;
  margin-bottom: 45px;
  padding-top: 25px;
  @media only screen and (min-width: 1600px) {
    font: normal normal bold 24px/36px Century Gothic;
    margin-bottom: 55px;
  }
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
  font: Bold 19px/38px century-gothic;
  letter-spacing: 0.02px;
  color: #f27c3e;
  opacity: 1;
  width: 210px;
}

.btn.learn {
  margin-right: 60px;
  &:hover {
    color: #ffffff;
    background: #f27c3e;
  }
}
.btn.find {
  margin-right: 0px;
}

.homepage-hero .btn {
  @media only screen and (max-width: 1200px) {
    display: block;
    margin: 20px auto;
    width: 210px;
    /*font: Bold 20px/38px century-gothic;*/
  }
}
.homepage-hero {
  margin: 0px;
  z-index: 1;

  @media only screen and (min-width: 1200px) {
    height: 570px;
  }
  @media only screen and (min-width: 1600px) {
    height: 700px;
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
  margin-bottom: 102px;
  width: 120px;
}

.home-cards {
  text-align: center;
  color: black;
  margin: 100px auto;

  .cards-container {
    @media only screen and (min-width: 1000px) {
      display: flex;
      justify-content: space-evenly;
    }
    @media only screen and (min-width: 1600px) {
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
    @media only screen and (max-width: 1600px) {
      width: 300px;
      height: 400px;
    }
  }
  .card-body {
    margin: auto;
    text-align: center;
    font-size: 24px;
    img {
      position: absolute;
      bottom: 70px;
      left: 130px;
    }
    p {
      padding: 0 35px;
    }
    @media only screen and (max-width: 1600px) {
      font-size: 20px;
      img {
        left: 85px;
        bottom: 50px;
      }
      p {
        padding: 0 15px;
      }
    }
  }
  .card-title {
    margin-top: 17px;
    margin-bottom: 30px;
    font-size: 28px;
    font-weight: bold;
    @media only screen and (max-width: 1600px) {
      font-size: 24px;
    }
  }

  h2 {
    font-size: 35px;
    @media only screen and (min-width: 1600px) {
      font-size: 45px;
    }
  }
  .why-group {
    margin-top: 31px;
    font-size: 20px;
    @media only screen and (min-width: 1600px) {
      font-size: 24px;
    }
    a {
      color: white;
      text-decoration: underline;
    }
  }
  .get-started {
    margin-top: 72px;
    margin-bottom: 207px;
  }
}

.what-is-cep-block {
  h2 {
    text-align: center;
    font-size: 35px;
    @media only screen and (min-width: 1600px) {
      font-size: 45px;
    }
  }
  .content-row {
    margin: 0px 0px 268px 0px;
    font-size: 31px;
    width: 100%;
    @media only screen and (min-width: 1200px) {
      width: 1050px;
      & > div {
        padding-right: 40px;
      }
    }

    @media only screen and (min-width: 1600px) {
    width: 1350px;
    }
    @media only screen and (max-width: 1600px) {
      font-size: 22px;
    }
  }
  img {
    width: 100%;
  }
}

.support-block {
  color: black;
  h2 {
    font-size: 35px;
    @media only screen and (min-width: 1600px) {
      font-size: 45px;
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
</style>
