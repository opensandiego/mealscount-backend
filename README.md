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

The current iteration of MealsCount is centered on the "validate" branch (where you are now), and centered on the python classes in the module "strategies", as well as a web frontend for browsing.

The python toolset can either be run from the example Jupyter notebook, the command line tool "cep_estimatory.py" script, or via a REST API from the server.py flask app.

There is a Vue.js frontend app built to display / interact with the server.py app. 

This web app is currently deployed to https://www.mealscount.com/ (hosted by Heroku).

The cep_estimatory.py script will take in as an argument a specially formatted CSV file, and paramteres defining different optimization strategies, and output a JSON file as well as a data table that describes the results of the optimization per district. 

# Example Usage - Algorithm Dev

If you are interested in exploring / experimenting / building on the algorithms, your first step would be to install a local python environment and run the Jupyter Notebook "CEP Estimator.ipnyb"

This environment can be created with a virtual environment using the jupyter_requirements.txt (using Python 3.7)

    $> pip install -r jupyter_requirements.txt
    $> jupyter notebook

# Example Usage - Frontend Dev

If you are just looking to work on the Vue.js front-end, and don't want / know how to setup a python environment, you can just utilize the node toolset and run "npm run start". This will automatically proxy all data feeds to https://www.mealscount.com/, and let you adjust your local Vue.js environment.

    $> npm install . 
    $> npm run start

# Example Usage - Full Stack Dev

If you are interested in developing on the app in entirety, you can do this by creating both the python and node environments, and then running the consolidated "npm run local_dev" command that will launch both the node "watch" process and the python flask server.

    $> npm install .
    $> pip install -r requirements.txt
    $> npm run local_dev

# Important Note on Build Process

There is a postinstall script in the root package.json that will run the optimizations for all of California. This can take a while, but is there specifically so we can do our initial set of optimizations at build time in Heroku, and then just do district-by-district optimizations later.

# Adding other state data

If you have access to data for other states (aside from California), you can add them to the "data" folder under your state code. There is a README.md referenced in that folder that indicates what your data csv (named latest.csv) should contain.

# Contributing

Please see the Issues for how to help, and contact the [Open San Diego Team on Slack](https://opensandiego.org) on the *#mealscount* channel if you are interested in helping or exploring facilitating school districts in your state in optimizing their CEP reimbursements!

# Additional Resources

* https://cfpa.net/ChildNutrition/ChildNutrition_CFPAPublications/CFPA-CEPLCFFWebinar-2018.pdf
* https://cfpa.net/ChildNutrition/ChildNutrition_Legislation/LCFF-CEP-Factsheet-2014.pdf
* https://www.fns.usda.gov/nslp/community-eligibility-provision-resource-center
* https://www.cde.ca.gov/ds/sd/sd/filescupc.asp  - The CALPADS data file (UPC) used for initial development
