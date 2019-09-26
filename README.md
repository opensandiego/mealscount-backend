# MealsCount
MealsCount is a tool created by [Open San Diego](https://opensandiego.org) in partnership with [California Food Policy Action](https://cfpa.org) and the [San Diego Hunger Coalition](https://www.sandiegohungercoalition.org), to help school districts maximize their reimbursements when participating in the [USDA's Community Eligibility Provision (CEP](https://www.fns.usda.gov/school-meals/community-eligibility-provision).

# What is the Community Eligibility Provision?
The USDA's Community Eligibility Provision (CEP) is a program whereby the federal government provides free and reduced cost meals *without filling out any paperwork*. This eliminates the burden on families in applying, as well as the stigma of students receiving food aid. Hungry students don't learn, so ensuring every student gets the nutrition they need increases the effectiveness of our education system.

# Why MealsCount?
Within the CEP, there is flexibilty for districts who participate in how they group the schools in their district to meet the qualifying criteria. Whether or not schools within a district get the reimbursements from the USDA is based upon how many "identified students" are in their group. This "Identified Student Percentage" (ISP), mutliplied by a factor (ISP X 1.6) must be above 62.5% for full funding, or exceed 40% for partial funding. Any percentage *over* 62.5% is irrelevant. This is where MealsCount comes in. Because you can group schools into any arbitrary grouping, you have the opportunity to take the highest poverty schools who have a high ISP, e.g. 85% (or lots of disadvantaged students, e.g. students already receiving aid, migrant students, homeless and foster students), and bundle them with a middle-level ISP school, e.g. 55%, and potentially have both over 62.5% and get free funding!

For a small district of 3 to 4 schools, this is trivial to do by hand. However for districts with 10 or more schools, we need to use an algorithm to optimize. Add to this that funding is dependant on the number of meals actually served, not the overall enrolled students, and we add mopre complexity. MealsCount provides a tool to run optimization strategies and bundle schools together and maximize reimbursements and free meals. The results of optimization are potentially incredible, with in Calfornia alone the possibility of adding *hundreds of thousand of free meals* to kids over not-optimizing! 

# The Details
We are still in the process of understanding how to best to deliver and facilitate this program. Our "client" is the Nutrition Director and/or CFO of a school district, and our partners are the food policty experts and advocates who can help us navigate various policy details in how best to utilize CEP for any given district in any given state. We are looking for MealsCount to be a tool that brigades can leverage the facilitate districts in maximizing their potential reimbursements via CEP.


# MealsCount Anatomy

The current iteration of MealsCount is centered on the "validate" branch (where you are now), and centered on the "cep_estimatory.py" file, which is a command line utility.

The cep_estimatory.py script will take in as an argument a specially formatted CSV file, and paramteres defining different optimization strategies, and output a JSON file as well as a data table that describes the results of the optimization per district. 

A recent example spreadsheet for the state of California is bundled in the "data" folder as "calpads....csv", so you can use this as a starting point to evaluate California, or to mimic for your state.

Also included is an html file that shows a more user friendly representation of the output created. This html file is fully consolidated with CSS/Javascript at this point, but you will need an Internet connection, as it relies on external "CDN JS" files to drive the interactivity (Vue.js, Bootstrap, and D3 are used). To see this, open viz.html in your browser, but due to security limitations you will need to run this file via a local webserver (see below).

# Example Usage

Run the cep_estimator.py file with arguments to generate an "output.json":

`python cep_estimatory.py data/calpads_school_level_1718.csv OneToOne OneGroup Binning`

Then, run a web server in the local folder:

`python -m http.server`

Open http://localhost:8000/viz.html and you will see a navigable result.

# Contributing

Please see the Issues for how to help, and contact the [Open San Diego Team on Slack](https://opensandiego.org) on the *#mealscount* channel if you are interested in helping or exploring facilitating school districts in your state in optimizing their CEP reimbursements!

# Additional Resources

* https://cfpa.net/ChildNutrition/ChildNutrition_CFPAPublications/CFPA-CEPLCFFWebinar-2018.pdf
* https://cfpa.net/ChildNutrition/ChildNutrition_Legislation/LCFF-CEP-Factsheet-2014.pdf
* https://www.fns.usda.gov/nslp/community-eligibility-provision-resource-center

