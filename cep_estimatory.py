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
@click.option("--target-district",default=None,help="Specific district code to run")
@click.option("--strategy",default="OneToOne",help="Grouping strategy")
@click.option("--baseline",default=None,help="Baseline Grouping strategy to compare")
@click.option("--show-groups",default=False,is_flag=True,help="Display grouping per district by school-code (must have target district specified)")
@click.option("--show-schools",default=False,is_flag=True,help="Display individual school data (must have target district specified)")
@click.option("--min-schools",default=None,help="If specified, only districts with at least N schools will be evaluated",type=int)
@click.argument("cupc_csv_file",nargs=1)
def cli(cupc_csv_file,baseline=None,target_district=None,strategy="OneToOne",show_groups=False,show_schools=False,min_schools=None):
    i = lambda x: int(x.replace(',',''))
    schools = [r for r in csv.DictReader(open(cupc_csv_file)) if i(r['total_enrolled']) > 0]

    # Reduce to target district if specified
    if target_district != None:
        schools = [s for s in schools if s["District Code"] == target_district]

    # Naive Groupings
    #DistrictClass = OneToOneCEPDistrict
    
    DistrictClass = STRATEGIES[strategy]
    districts = parse_districts(schools,DistrictClass)

    if min_schools != None:
        x = len(districts)
        districts = [ d for d in districts if len(d.schools) >= min_schools ]
        x = x - len(districts)
        click.secho("Ignoring %i districts with less than %i schools" % (x,min_schools) )


    n_schools = sum([len(d.schools) for d in districts])
    total_overall = sum([d.total_enrolled for d in districts])

    click.secho("\nParsed {:,} schools in {:,} districts representing {:,} students\n".format( 
            n_schools,
            len(districts), 
            total_overall,
         ),
        fg="blue"
    )
    
    # Process target strategy
    with click.progressbar(districts,label='Grouping Districts with %s' % strategy) as bar:
        for district in bar:
            district.create_groups() 
    
    if baseline:
        BaselineDistrictClass = STRATEGIES[baseline]
        baseline_districts = parse_districts(schools,BaselineDistrictClass)
        with click.progressbar(baseline_districts,label='Grouping District Baseline with %s' % baseline) as bar:
            for district in bar:
                district.create_groups() 
        
        results = [] 
        for d1 in districts:
            d0 = [d for d in baseline_districts if d == d1][0]
            results.append([
                d1.code,
                d1.name[:64],
                float(len(d1.schools)),
                d1.matches_grouping_of(d0) and "*" or "",
                "%s/%s" % (len(d0.groups),len(d1.groups)),
                float(d0.total_enrolled),
                float(d1.students_covered) - float(d0.students_covered),
                (d0.percent_covered*100),
                (d1.percent_covered*100),
            ])

        print( tabulate.tabulate(
            results,
            [   'code',
                'district',
                '# schools',
                'same groups',
                '# groups',
                'total enrolled',
                'change in students covered',
                'base % covered',
                'opt % covered',
            ],
            tablefmt="pipe",
            floatfmt=("","",",.0f","","",",.0f","+,.0f",",.0f",".0f",".0f"),
        ))
    else:       
        data = [ [
                district.code,
                district.name[:64],
                float(len(district.schools)),
                float(len(district.groups)),
                float(district.students_covered),
                float(district.total_enrolled),
                (district.percent_covered*100) ] for district in districts ]
        headers = ['code','district','# schools','# groups','students covered','total enrolled','% covered']

        print( tabulate.tabulate(data,headers,tablefmt="pipe",floatfmt=("","",",.0f",",.0f",",.0f",",.0f",".0f")))

    click.secho("\n"+"="*100,bold=True)

    if baseline:
        click.secho("Baseline Strategy: %s" % baseline)
    click.secho("Optimization Strategy: %s" % strategy)

    click.secho(    "{:,} Schools Processed for {:,} districts".format(n_schools,len(districts)) ,
                    fg="blue", bold=True )

    if baseline:
        overall_eligible = sum([d.students_covered for d in districts]) - sum([d.students_covered for d in baseline_districts]) 
        c = "red"
        if overall_eligible > 0: c = "green"
        click.secho("{:+,} Students are eligible with {:} vs {:}".format(overall_eligible,strategy,baseline),fg=c)
    else:
        eligible_overall = sum([d.students_covered for d in districts])
        click.secho("{:,.0f} Students are eligible out of {:,.0f} ({:.0f}%) total enrolled".format(
            eligible_overall,
            total_overall,
            (eligible_overall/total_overall * 100),
        ))

    if target_district:
        td = districts[0]
        if show_groups:
            print( "Groupings for %s" % td )
            for g in td.groups:
                click.secho( "%s (%i schools)" % (g.name,len(g.school_codes)), bold=True )
                print( ",".join(g.school_codes) )
        if show_schools:
            data = [ (s.code,s.name,float(s.total_eligible),float(s.total_enrolled),s.isp) for s in td.schools ]
            data.sort(key=lambda o: o[4])
            print(tabulate.tabulate(
                    data,
                    ('Code','Name','Eligible','Enrolled','ISP'),
                    tablefmt="pipe",
                    #floatfmt = ("","",",.0f",",.0f",".3f" ),
            ))

if __name__ == '__main__':
    cli()    

