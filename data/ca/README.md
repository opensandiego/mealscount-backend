# California School Data

The California MealsCount data is retrieved from CALPADS (California Longitudinal Pupil Achievement Data System), the California system that is used to track all students. They publish an aggregate school data file around August that has the prior year's data. This file is call the "CUPC" or Calpads Undupicated Pupil Count file. 

Download URL: https://www.cde.ca.gov/ds/sd/sd/filescupc.asp

# Processing the XLSX file

Once downloaded, you need to save the sheet named "School-Level CALPADS UPC Data" (starting with the column header rows).

Certain columns need to be renamed to fit the expected columns

"Total Enrollment" to "total_enrolled"
"Free & Reduced Meal Program" to "frpm"
Foster to "foster"
Homeless to "homeless"
"Migrant Program" to "migrant"
"Direct Certification" to "direct_cert"
"Unduplicated FRPM Eligible Count" to "unduplicated_frpm"
"English Learner (EL)" to "english_learner"

Note that some of these column names in the original XLS span mulitple lines (have CR or LF in them). For presentation we have ignored those in this mapping.

# Adding participation rate

TODO We are currently reviewing participation rate data provided by our partners and will be indicating how to merge this into the source data soon.
