<template>
 <section class="container mt-5">
   <h1 class="headline text-center">Meals Count FAQ</h1>
   <br>
   
   <VueFaqAccordion :items="myItems" />
 </section>

  <!-- make to sections one with CEP and then Foodpoint 
   make an Faq.json in the assets, import this Faq as an object in the Faq and run in. 
  the paragraph (p) tabs should be Answer and (q) should be Question -->
<!-- <section>  -->
  <!-- <h1> FAQ </h1>

  <h3> Is this tool free to use? </h3>
  <div class="panel">
  <p> Yes, MealsCount is a free tool.  </p>
  </div>
 
 <h3> Frage2 </h3>
 <p> antwort2 </p>


</section> -->
</template>


<script >  
import VueFaqAccordion from "vue-faq-accordion";

export default {
  name: "App",
  components: {
    VueFaqAccordion
  },
  data() {
    return {
      myItems: [
        {
          title: "What is Community Eligibility Provision (CEP)?",
          value:
            "CEP is a federally authorized option for It is a provision that allows schools to offer school breakfast and lunch free of charge to all students without the use of school meal applications. CEP also determines how schools will be reimbursed for meals served to students.  at no charge, while eliminating the need to collect school meal applications. ",
          category: "CEP"
        },
         {
          title: "How Does CEP Funding Work?",
          value: `Federal funding for CEP follows the following formula:
Identified Student Percentage * 1.6 Multiplier = Percent of  Meals Reimbursed at the Higher (“Free”) Rate
All other meals are reimbursed at the lower (“paid”) rate.
The multiplier is set by federal rules. Currently the multiplier is set at 1.6 nationwide. Federal action could change the multiplier to a value between 1.3 and 1.6. Schools implementing CEP are guaranteed the same multiplier for at least a four-year cycle. 
` ,
              category: "CEP"
        },
        {
          title: "What are the benefits of CEP?",
          value:
            `<u>For the students: </u> <br>
Students are guaranteed access to eat Bbreakfast and lunch at no cost to them
Removes stigma associated with being labeled as poor 
Meal lines move faster because there is no need to identify reduced, free or paid meals.
Reduced food insecurity rates by increasing access to healthy meals
<br> <br>

<u> For the Administration: </u> <br>
Significant less paperwork for the nutrition department
No need to collect Free and Reduced Meals Application
No need to track and collect money at the lunchroom
Increase State and Federal reimbursement 
Administrative savings allows putting those resources into improving meal quality service
Schools are eligible to participate in the program for 4 years utilizing the initial Identified Student Percentage (ISP) or re-apply to increase their ISP. 
Reduced food insecurity rates by increasing access to healthy meals

<br> <br>
<u> For the school </u> <br>
Provide a service to the community. CEP enables eligible schools to serve free breakfast and lunch to all students, regardless of income.
Reduces or eliminates stigma at the school by eliminating identification of free and reduced lunch recipients
Improving meal participation rates
No unpaid student meal debt
Increased school attendance and improved academic performance
Reduction of sick days and school nurse visits
Reduced food insecurity rates by increasing access to healthy meals`,
          category: "CEP"
        },

         {
          title: "Who are the “Categorically Eligible” Students?",
          value:
           `Students that have been categorically identified and approved to receive free or reduced meals without the need for families to submit a school lunch application. <br><br>
<ol> Enrolled in the Supplemental Nutrition Assistance Program (SNAP) , also known as CalFresh in California </ol>
<ol> Temporary Assistance for Needy Families (TANF), known as The California Work Opportunities and Responsibility to Kids <strong>(CalWORKs)  </strong></ol>
<ol>the Food Distribution Program on Indian Reservations <strong> (FDPIR) </strong></ol>
<ol><strong>Medicaid/Medi-Cal</strong> (not all students enrolled in Medicaid/Medi-Cal qualify for free meals, students that qualify for reduced-price meals cannot be included in the ISP percentage). </ol>
<ol>Students that live in a household where another student is enrolled in one of these programs (this is referred to as ‘extended eligibility’ or a ‘sibling match’).</ol>
<ol>Students that are categorized, at the local level, as being part of any of the following categories: homeless, migrant, runaway, in foster care, or enrolled in Head Start or Early Head Start (note that these categories do not confer eligibility to other students in the household.)</ol>
`,
          category: "CEP"
        },
         {
          title: "How to determine if a student can be categorized as homeless?",
          value:
            `<li> The McKinney-Vento Act defines homeless children and youths as individuals who lack a fixed, regular, and adequate nighttime residence. This definition also includes: Children and youths who are sharing the housing of other persons due to loss of housing, economic hardship, or a similar reason. </li>
            <br><li>The California Department of Education definition of homeless children is currently under review. </li>
            <br><li>Children are categorized into this group at the local level (by the Local Education Authority/School District). </li> `,
          category: "CEP"
        },

         {
          title: "What is an identified student percentage, ISP?",
          value: `Is the percentage of students who have been categorically approved by CALPADS or other methods to receive Free and/or reduced-price school meals. 
          To calculate ISP, a school must count all of the students who are categorically eligible for <strong> free </strong> school
           meals and divide that number by total student enrollment. `,
          category: "CEP"
        },

         {
          title: "Which students are eligible to participate in CEP?",
          value:
            "Once the school has been approved to participate, all students will have access to free breakfast and lunch, regardless of income. ",
          category: "CEP"
        },

         {
          title: "Which schools are allowed to use CEP?",
          value:
            "For a school to be eligible to participate in CEP, it must have an Identified Student Percentage (ISP) greater than 40%.",
          category: "CEP"
        },
        {
          title: "Can a school that is below 40% ISP join CEP?",
          value:
            `If the school ISP is below 40%, the school has the choice to join with one or more schools with a higher ISP within the Local Education Authority (LEA) to increase the percentage of Identified students as a group. 
            The MealsCount tool is an optimization tool designed to find the best grouping of schools.`,
          category: "CEP"
        },
        {
          title: "Are there other federal programs available for LEAs to offer Universal Free Meals to all students? ",
          value:
          `Yes, there is another provision that allows schools to serve Universal Free meals. To learn more, please click on the link below: 
<a href="https://fns-prod.azureedge.net/sites/default/files/Prov2Guidance.pdf">Provision 2</a>`,
          category: "CEP"
        },


         {
          title: "Is this tool free to use?",
          value:
            "Yes, MealsCount is a free tool.",
          category: "MealsCount"
        },
         {
          title: "Some of the numbers displayed for my school district are different than our actual numbers <br>(i.e. enrollment, total eligible, daily participation)",
          value:
           `There are several reasons why your numbers might not match the numbers prepopulated on MealsCount:++ <br>
<ul>a) Total enrolled: enrollment information from school year 2018-2019, it is extremely possible that enrollment at your school decreases or increases each year. 
As well, preschool students are not included in the number. </ul>
<ul>b) Total eligible: this is the number of Direct Certified students with school data we receive from CALPADS, the data is from school year 2018-2019. This number does not include: homeless, migrant, runaway, in foster care, 
or enrolled in Head Start or Early Head Start , and students identified using household extended eligibility. Your district's numbers may be significantly higher. </ul> 
<ul>c) Daily Breakfast served: data from school year ____ provided by ___ </ul><br>
<ul>d) Daily Lunch served: data from school year ____ provided by ___  </ul><br>
<i>MealsCount allows you to edit the numbers on each column to match the actual numbers of your school/district. </i>`,
          category: "MealsCount"
        },

         {
          title: "Is this tool only available for California districts?",
          value:
            "MealsCount is available to all California districts with plans to…",
          category: "MealsCount"
        },
        {
          title: "Where is the source of the data included for each school/district?",
          value:
            "The data shown for each district is from the 2018-2019 CALPADS aggregate data, as well as April 2019 meals average meals data.",
          category: "MealsCount"
        },
        {
          title: "Are Charter schools included?",
          value: "Yes, charter schools that claim Free and Reduced Priced Meals (FRPM) for reimbursement are included.",
          category: "MealsCount"
        },
        {
          title: "Which types of schools are included/excluded? (continuation, juvenile, preschool, especial ed, etc.)",
          value: `<strong>Included</strong>: Schools that claim FRPM for reimbursement; and are one of the following types of public and charter schools: 
          Elementary, Middle schools, Junior High Schools, High Schools, and K-12 schools. <br><br>
          <strong>Excluded</strong>: Alternative schools, Continuation High Schools, County Community, Juvenile Court Schools, Preschools, 
Special Education Schools and Youth Authority Facilities are not included (not sure if this is correct???). However, MealsCount includes a function to include new schools to your list in order to calculate ISP. `,
          category: "MealsCount"
        },
        {
          title: "Please explain each “Pairs”, “Exhaustive”, “Binning”, “Spread” and other strategies:",
          value: "Tba",
          category: "MealsCount"
        }
        ,
        {
          title: "How is the best grouping strategy calculated?",
          value: "Tba",
          category: "MealsCount"
        }
        ,
        {
          title: "Please explain each best strategy: pairs, OneGroup, Spread",
          value: "Tba",
          category: "MealsCount"
        },
        {
          title: "What is the reimbursement rate used? (explain if it will be updated each year, add that it doesn’t impact grouping strategy?)",
          value: "The reimbursement rates include the yearly rates approved by the United States Department of Agriculture (USDA) and California Department of Education (CDE). Please note that the rates don’t impact the grouping optimization feature, but we understand that it is important to reflect the estimated reimbursement amount for each group to assist you in making the best financial decision for your program. ",
          category: "MealsCount"
        },
        {
          title: "Is state reimbursement included with the Estimated Annual Reimbursement Range amount?",
          value: `No, the amount indicated on the Estimated Annual Reimbursement Range does not include the state reimbursement. 
          Please consider adding the expected state reimbursement when making a financial decision for your program.`,
          category: "MealsCount"
        },
        {
          title: " Is the $0.6 reimbursement added for severe need schools?",
          value: `tba`,
          category: "MealsCount"
        },
        {
          title: "Once I have the grouping results, what are the next steps?",
          value: `MealsCount is an optimization tool that helps you group schools in the most favorable way to increase your funding for school meals, and help fight child hunger. We recognize that there are multiple factors that may impact your decision to apply for CEP such as participation, student debt, revenue collected from paid students or other sources (e.i. A la carte items), expected increase or drop on school enrollment, etc. Local and internal factors such as the ones mentioned are critical to consider before making a decision. Our recommendation is that once you have your grouping results, we suggest analyzing the different scenarios and the estimated reimbursement and participation numbers for each group, if applicable, adding the state reimbursement and any other amount not reflected on MealsCount,
           and comparing them to your current figures. For free technical assistance to analyze your results, you can contact ______`,
          category: "MealsCount"
        },
      ]
    };
  }
};

</script>

<style scoped>



.panel {
  padding: 0 18px;
  background-color: white;
 
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: start;
  color: #2c3e50;
  margin-top: 60px;
}



</style>

