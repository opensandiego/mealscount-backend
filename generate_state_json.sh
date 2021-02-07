# Builds json district data in /static/dist/ based on data/*/latest.csv

for d in `ls data`; 
do
    if [ -d $d ]
    then
        python cep_estimatory.py data/$d/latest.csv --output-folder dist/static/$d/;
    fi
done;

