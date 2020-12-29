# Builds json district data in /static/dist/ based on data/*/latest.csv

for d in `ls data`; 
    do python cep_estimatory.py data/$d/latest.csv --output-folder dist/static/$d/;
done;

