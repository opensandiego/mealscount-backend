<template>
    <section>
      <div class="position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center bg-light">
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
            <!-- <p class="lead">Open San Diego</p> -->
            <!-- <a href="https://opensandiego.org"><img class="logo" src="https://secure.meetupstatic.com/photos/event/2/f/9/b/global_479232187.jpeg"> </a> -->
            <a href='https://www.cfpa.org'> <img class='logo' v-bind:src="logos.cfpa_logo" /> </a>
            



            <!-- <p class="lead">CFPA</p> -->
            <a href="https://www.cfpa.org"> <img class="logo" src="https://cfpa.org/wp-content/uploads/2016/08/logo_main.png">  </a>
            <!-- <p class="lead">SD Hunger Coalition</p> -->
             <a class="text-muted" href="https://www.sdhunger.org"><img class="logo" src="https://static1.squarespace.com/static/55130907e4b018f9300f3e63/t/5536889ae4b02181f8565b51/1581465416766/?format=1500w"></a>
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
import CFPALogo from '../assets/CFPA Logo.jpg';
export default {
  data() {
    return {
     logos: { cfpa_logo: CFPALogo }
    }
  }
}
</script