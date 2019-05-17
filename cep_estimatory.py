import csv
import click
import tabulate
from strategies.base import CEPSchool,CEPDistrict
from strategies import STRATEGIES
from urllib import parse
import json

#### CLI ####

def parse_districts(school_data,strategies):
    districts = {}
    for row in school_data:
        school = CEPSchool(row)
        district = CEPDistrict(school.district,school.district_code)
        for s in strategies:
            StrategyClass,params,strategy_name = s
            district.strategies.append( StrategyClass(params,name=strategy_name) )
        districts.setdefault(school.district,district)
        districts[school.district].schools.append(school)
    districts = list(districts.values())
    districts.sort()
    return districts

@click.command()
@click.option("--target-district",default=None,help="Specific district code to run")
@click.option("--show-groups",default=False,is_flag=True,help="Display grouping per district by school-code (must have target district specified)")
@click.option("--show-schools",default=False,is_flag=True,help="Display individual school data (must have target district specified)")
@click.option("--min-schools",default=None,help="If specified, only districts with at least N schools will be evaluated",type=int)
@click.option("--list-strategies",default=False,is_flag=True,help="Display all available strategies and exit")
@click.option("--output-json",default="output.json",help="If Specified, output will stored in filename specified in JSON format (defaults to output.json)")
@click.argument("cupc_csv_file",nargs=1)
@click.argument("strategies",nargs=-1)
def cli(    cupc_csv_file,
            strategies=["OneToOne"],
            target_district=None,
            show_groups=False,
            show_schools=False,
            min_schools=None,
            list_strategies=False,
            output_json=None ):
    """CEP Estimator - runs strategies for grouping School Districts into optimial CEP coverage

To run, specify the schools/districts CSV file, as well as any number of strategies (use --list-strategies to see those available)

Expected CSV File columns 
(see data folder for example, extra columns are ignore, column order is not important):

"District Code","School Code","District Name","School Name","total_enrolled","frpm","foster","homeless","migrant","direct_cert"

"""
    if list_strategies:
        for s in STRATEGIES:
            click.secho("\n%s"%s,fg="blue",bold=True)
            click.secho(STRATEGIES[s].__doc__)
        return

    i = lambda x: int(x.replace(',',''))
    schools = [r for r in csv.DictReader(open(cupc_csv_file)) if i(r['total_enrolled']) > 0]

    # Reduce to target district if specified
    if target_district != None:
        schools = [s for s in schools if s["District Code"] == target_district]

    # Naive Groupings
    #DistrictClass = OneToOneCEPDistrict
  

    def parse_strategy(strategy):
        strategy_param = parse.urlparse(strategy)   
        params = dict(parse.parse_qsl(strategy_param.query))
        klass = STRATEGIES[strategy_param.path]
        return (klass,params,strategy)
    strategies = [parse_strategy(s) for s in strategies]

    districts = parse_districts(schools,strategies = strategies)

    print("Districts with 10 or less schools: %0.0f%%" % (len([d for d in districts if len(d.schools) <= 10])/float(len(districts)) * 100))

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
    with click.progressbar(districts,label='Running Strategies on Districts') as bar:
        for district in bar:
            district.run_strategies() 
            district.evaluate_strategies()

    data = []   
    for district in districts: 
        p0 = (float(district.strategies[0].students_covered) / district.total_enrolled)
        p1 = (float(district.best_strategy.students_covered) / district.total_enrolled)
        row = [
            district.code,
            district.name[:64],
            float(len(district.schools)),
            float(district.total_enrolled),
            district.strategies[0].name,
            district.best_strategy.name,
            p0 * 100.0,
            p1 * 100.0,
            (p1-p0) * 100.0,
        ]
        for s in district.strategies:
            row.append(s.students_covered) 
        data.append(row)
    headers = ['code','district','# schools','total enrolled','baseline','best_strategy','ISP Baseline','ISP Best','ISP %change']
    float_fmt = ["","",",.0f",",.0f","","",'.0f','.0f','+.0f']
    for s in districts[0].strategies:
        headers.append( "eligible: %s" % s.name )
        float_fmt.append(",.0f")
    print( tabulate.tabulate(data,headers,tablefmt="pipe",floatfmt=float_fmt) )

    click.secho("\n"+"="*100,bold=True)

    click.secho("Baseline Strategy: %s" % strategies[0][0].name)
    if len(strategies) > 1:
        for s in strategies[1:]:
            click.secho("Optimization Strategy: %s" % s[0].name)

    click.secho(    "{:,} Schools Processed for {:,} districts".format(n_schools,len(districts)) ,
                    fg="blue", bold=True )

    baseline_eligible_overall = sum([d.strategies[0].students_covered for d in districts])
    best_eligible_overall = sum([d.best_strategy.students_covered for d in districts])
    improvement = best_eligible_overall - baseline_eligible_overall
    click.secho("{:+,.0f} students eligible over baseline ({:,.0f} => {:,.0f}), {:+.0f}% change to ISP {:.0f}%".format( 
        improvement,
        baseline_eligible_overall,
        best_eligible_overall,
        (improvement/total_overall) * 100.0,
        (best_eligible_overall/total_overall) * 100.0,
    ),fg=(improvement > 0 and "green" or "red"))

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

    if output_json:
        with open(output_json,"w") as out_file:
            # TODO make this more interesting
            o = [d.as_dict() for d in districts]
            out_file.write(json.dumps(o,indent=1))

if __name__ == '__main__':
    cli()    

