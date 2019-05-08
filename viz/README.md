## Run

Make sure yarn is installed

    (mac): (mealscount-backend/viz)$ brew install yarn
    (linux): (mealscount-backend/viz)$ apt install yarn

Go to project root and generate data in viz/src/data

    (mealscount-backend/viz)$ python cep_estimatory.py data/sample_calpads_and_meals.csv OneToOne Binning --output-json viz/src/data

Run server

    yarn start

Check it out at localhost:8080

## Documentation

HTML Generation: https://github.com/jantimon/html-webpack-plugin
Styles: https://www.muicss.com/
