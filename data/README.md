# MealsCount Data Feeds

MealsCount relies on data that describes every school in the given state, with percentages of the "identified student population" (homeless, migrant, frpm, etc), as well as participation data where available.

This folder, and the folders contained within is where we are keeping the latest data feeds from various states (currently only California). To add a data feed, create a folder with the state code (e.g. "ca") and put the file in there named latest.csv. This should be the latest applicable data file (as of this writing the prior schoolyear 2018-2019).

Please leave a document in the state folder to indicate both the source of where you got this data (e.g. a URL) as well as the steps to extract the relevant CSV file (e.g. column changes, picking from a certain sheet). Again, please see the "ca" folder for an example.

# Expected Data Structure

The data file must be in a UTF-8 encoded CSV format, where every row corresponds to 1 School. The first row should be column headers.

The following columns are required (quotes indicate exact name):

"District Code" - the code of the district used to group all schools in that district
"School Code" - the code of the school (or unique name if no code available)
"District Name" - the name of the district (should be the same for all schools in that district)
"School Name" - the name of the school
"total_enrolled" - the total number of students enrolled in that school
"frpm" - the total number of enrolled students who are in the Free & Reduced Meal Program (frpm)
"foster" - the total number of enrolled students who are identified as Foster
"homeless" - the total number of enrolled students who are identified as homeless
"migrant" - the total number of enrolled students who are identified as "migrant"
"direct_cert" - the total number of enrolled students who have been directly certified
"unduplicated_frpm" - the unduplicated number of frpm students
"english learner" - the total number of unrolled students identified as english learners




