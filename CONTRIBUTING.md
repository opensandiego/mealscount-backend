# MealsCount Contributing Guide
MealsCount is an open source tool available to anyone who is interested, but generally targeted towards civic technologists located in the USA who are interested in helping their local School Districts maximize the funding they can get from the USDA Community Eligibility Provision.

That being said, MealsCount is a tool to help understand a somewhat complicated piece of policy, with a target audience being nutrition directors and CFOs of school districts, as well as food policy advocates. The best way to help out is to reach out to the core developers of the project and ask them to help connect you with a local or national food policy organization.  

# The codebase
The code consists of a few parts:

1. The Python model / algorithms
- The strategies folder contains a data / policy model in python, as well as optimization code where the actual optimization is done

2. Jupyter Notebook
- The CEP Estimator jupyter notebook provides some examples on utilizing the python object model in the strategies folder, as well as extending it

3. Flask Server (server.py)
- A python-flask server that will serve an html/js frontend, as well as provide an api to running the calculations

4. Javascript Front End (webpack / src / package.json)
- A Vue.js frontend for the Mealscount website that will let users review and tune the optimizations for a given state


# Contributing
The best approach would be to reach out on the Open San Diego slack channel and inquire about helping out. Additionally you can clone the repo and read some of the references in the README to understand some of the details of CEP.