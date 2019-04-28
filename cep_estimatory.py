import csv
import click 
import tabulate
from strategies.base import CEPSchool
from strategies import STRATEGIES

#### CLI ####

def parse_districts(school_data,DistrictClass=STRATEGIES["OneToOne"]):
    districts = {}
    for row in school_data:
        school = CEPSchool(row)
        districts.setdefault(school.district,DistrictClass(school.district,school.district_code))
        districts[school.district].schools.append(school)
    districts = list(districts.values())
    districts.sort()
    return districts

@click.command()
@click.option("--target_district",default=None,help="Specific district code to run")
@click.option("--strategy",default="OneToOne",help="Grouping strategy")
@click.option("--baseline",default=None,help="Baseline Grouping strategy to compare")
@click.argument("cupc_csv_file",nargs=1)
def cli(cupc_csv_file,baseline=None,target_district=None,strategy="OneToOne"):
    i = lambda x: int(x.replace(',',''))
    schools = [r for r in csv.DictReader(open(cupc_csv_file)) if i(r['total_enrolled']) > 0]

    # Reduce to target district if specified
    if target_district != None:
        schools = [s for s in schools if s["District Code"] == target_district]

    # Naive Groupings
    #DistrictClass = OneToOneCEPDistrict
    
    DistrictClass = STRATEGIES[strategy]
    districts = parse_districts(schools,DistrictClass)
    total_overall = sum([i(s["total_enrolled"]) for s in schools])
    click.secho("\nParsed {:,} schools in {:,} districts representing {:,} students\n".format( 
            len(schools),
            len(districts), 
            total_overall,
         ),
        fg="blue"
    )
    
    # Process target strategy
    with click.progressbar(districts,label='Grouping Districts with %s' % DistrictClass) as bar:
        for district in bar:
            district.create_groups() 
    
    if baseline:
        BaselineDistrictClass = STRATEGIES[baseline]
        baseline_districts = parse_districts(schools,BaselineDistrictClass)
        with click.progressbar(baseline_districts,label='Grouping District Baseline with %s' % BaselineDistrictClass) as bar:
            for district in bar:
                district.create_groups() 
        
        results = [] 
        for d1 in districts:
            d0 = [d for d in baseline_districts if d == d1][0]
            results.append([
                d1.code,
                d1.name[:64],
                d1.matches_grouping_of(d0) and "*" or "",
                float(d0.total_enrolled),
                float(d1.students_covered) - float(d0.students_covered),
                (d0.percent_covered*100),
                (d1.percent_covered*100),
            ])

        print( tabulate.tabulate(
            results,
            [   'code',
                'district',
                'same groups',
                'total enrolled',
                'change in students covered',
                'base % covered',
                'opt % covered',
            ],
            tablefmt="pipe",
            floatfmt=("","","",",.0f","+,.0f",",.0f",".0f",".0f"),
        ))
    else:       
        print( tabulate.tabulate(
            [ (
                district.code,
                district.name[:64],
                float(district.students_covered),
                float(district.total_enrolled),
                (district.percent_covered*100) ) for district in districts ],
            ['code','district','students covered','total enrolled','% covered'],
            tablefmt="pipe",
            floatfmt=("","",",.0f",",.0f",".0f"),
        ))

    click.secho("\n"+"="*100,bold=True)

    if baseline:
        click.secho("Baseline Strategy: %s" % strategy)
    click.secho("Optimization Strategy: %s" % baseline)

    click.secho(    "{:,} Schools Processed for {:,} districts".format(len(schools),len(districts)) ,
                    fg="blue", bold=True )

        overall_eligible = sum([d.students_covered for d in districts]) - sum([d.students_covered for d in baseline_districts]) 
        c = "red"
        if overall_eligible > 0: c = "green"
        click.secho("{:+,} Students are eligible with {:} vs {:}".format(overall_eligible,strategy,baseline),fg=c)
    

if __name__ == '__main__':
    cli()    

