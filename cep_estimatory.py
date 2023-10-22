import csv
import click
import tabulate
from strategies.base import CEPSchool,CEPDistrict,DEFAULT_ISP_THRESHOLD
from strategies import STRATEGIES
from urllib import parse
import os,os.path
import codecs
import json

#### CLI ####

def parse_districts(school_data,strategies,state):
    districts = {}
    for row in school_data:
        if not row.get("included_in_optimization",True):
            continue
        school = CEPSchool(row)
        district_name,district_code = row.get('District Name',row.get('district_name','Default')),row.get('District Code',row.get('district_code','1'))
        if district_name not in districts:
            district = CEPDistrict(district_name,district_code,state=state)
            for s in strategies:
                StrategyClass,params,strategy_name = s
                district.strategies.append( StrategyClass(params,name=strategy_name) )
            districts.setdefault(district_name,district)
        districts[district_name].add_school(school)
    districts = list([d for d in districts.values() if len(d.schools)> 0])
    districts.sort()
    return districts

def parse_strategy(strategy):
    strategy_param = parse.urlparse(strategy)   
    params = dict(parse.parse_qsl(strategy_param.query))
    klass = STRATEGIES[strategy_param.path]
    return (klass,params,strategy)

def add_strategies(district,*strategies,isp_threshold=DEFAULT_ISP_THRESHOLD):
    for s in strategies:
        Klass,params,name = parse_strategy(s) 
        district.strategies.append( Klass(params,name,isp_threshold=isp_threshold) )

@click.command()
@click.option("--target-district",default=None,help="Specific district code to run")
@click.option("--show-groups",default=False,is_flag=True,help="Display grouping per district by school-code (must have target district specified)")
@click.option("--show-schools",default=False,is_flag=True,help="Display individual school data (must have target district specified)")
@click.option("--min-schools",default=None,help="If specified, only districts with at least N schools will be evaluated",type=int)
@click.option("--list-strategies",default=False,is_flag=True,help="Display all available strategies and exit")
@click.option("--output-json",default=None,help="If Specified, output will stored in filename specified in JSON format (defaults to output.json)")
@click.option("--output-csv",default=None,help="If Specified with target district, output for first strategy will stored as CSV in filename")
@click.option("--output-folder",default=None,help="Folder to output per-district json and district overview json for website")
@click.option("--evaluate-by",default="reimbursement",help="Optimize by reimbursement or coverage")
@click.option("--investigate",default=False,is_flag=True,help="Stop before exiting in a shell to investigate results")
@click.option("--state",default="ca",help="State code")
@click.argument("cupc_csv_file",nargs=1)
@click.argument("strategies",nargs=-1)
def cli(    cupc_csv_file,
            strategies=["OneToOne"],
            target_district=None,
            show_groups=False,
            show_schools=False,
            min_schools=None,
            list_strategies=False,
            output_json=None,
            output_csv=None,
            output_folder=None,
            investigate=False,
            state="ca",
            evaluate_by="reimbursement" ):
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

    def i(x):
        try:
            return int(x.replace(',',''))
        except ValueError:
            return 0
    schools = [r for r in csv.DictReader(codecs.open(cupc_csv_file)) if r['total_enrolled'] and i(r['total_enrolled']) > 0]

    # Reduce to target district if specified
    if target_district != None:
        schools = [s for s in schools if s.get("District Code",s.get("district_code",s.get("district",None))) == target_district]

    # Naive Groupings
    #DistrictClass = OneToOneCEPDistrict
    
    strategies = [parse_strategy(s) for s in strategies]

    districts = parse_districts(schools,strategies = strategies,state=state)

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
            district.evaluate_strategies(evaluate_by=evaluate_by)

    data = []   
    for district in districts: 
        if district.strategies:
            p0 = (float(district.strategies[0].students_covered) / district.total_enrolled)
            p1 = (float(district.best_strategy.students_covered) / district.total_enrolled)
        else:
            p0,p1 = 0,0
        row = [
            district.code,
            district.name[:64],
            float(len(district.schools)),
            float(district.total_enrolled),
            district.strategies and district.strategies[0].name or '',
            district.best_strategy and district.best_strategy.name or '',
            p0 * 100.0,
            p1 * 100.0,
            (p1-p0) * 100.0,
        ]
        for s in district.strategies:
            row.append(s.reimbursement) 
        data.append(row)
    headers = ['code','district','# schools','total enrolled','baseline','best_strategy','Reimb Baseline','Reimb Best','ISP %change']
    float_fmt = ["","",",.0f",",.0f","","",'.0f','.0f','+.0f']
    for s in districts[0].strategies:
        headers.append( "reimb: %s" % s.name )
        float_fmt.append(",.0f")
    
    #print( tabulate.tabulate(data,headers,tablefmt="pipe",floatfmt=float_fmt) )

    click.secho("\n"+"="*100,bold=True)

    if strategies:
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

    if investigate:
        print("Type dir() to see local variables")
        import code; code.interact(local=locals())

    if target_district:
        td = districts[0]
        #print(json.dumps(td.as_dict(),indent=1))
        if show_groups:
            print("\nGroupings for %s" % td )
            for s in td.strategies:
                print("\n%s: %0.2f" % (s.name,s.reimbursement))
                data = [
                    (   g.name,
                        len(g.schools), #','.join([s.name for s in g.schools]),
                        g.isp,
                        g.free_rate,
                        g.paid_rate,
                        g.est_reimbursement(),
                        g.total_enrolled,
                        g.covered_students,
                    )
                    for g in s.groups
                ] 
                print(tabulate.tabulate(
                    data,
                    ('Group','Schools','ISP','Free Rate','Paid Rate','Reimbursement','Enrolled','Covered'),
                    tablefmt="pipe",
                ))
        if show_schools:
            print("\nSchools")
            data = [ (
                s.code,
                s.name,
                float(s.total_eligible),
                float(s.total_enrolled),
                s.isp,
                s.bfast_served,
                s.lunch_served
                ) for s in td.schools ]
            data.sort(key=lambda o: o[4])
            print(tabulate.tabulate(
                    data,
                    ('Code','Name','Eligible','Enrolled','ISP','Daily Bkfst','Daily Lunches'),
                    tablefmt="pipe",
                    #floatfmt = ("","",",.0f",",.0f",".3f" ),
            ))

        if output_csv:
            strat = td.strategies[0]
            with open(output_csv,"w") as out_file:
                w = csv.DictWriter(out_file,fieldnames=(
                    "group","district_code","school_code","school_name","total_enrolled","total_eligible",
                    "daily_breakfast_served","daily_lunch_served","estimated_school_reimbursement"
                ))
                w.writeheader()
                for i,g in enumerate(strat.groups):
                    for s in g.schools:
                        row = {
                            "group": str(i+1),
                            "district_code": td.code,
                            "school_code": s.code,
                            "school_name": s.name,
                            "total_enrolled": s.total_enrolled,
                            "total_eligible": s.total_eligible,
                            "daily_breakfast_served": s.bfast_served,
                            "daily_lunch_served": s.lunch_served,
                            "estimated_school_reimbursement": g.school_reimbursement(s) * 180,
                        }
                        w.writerow(row)
            print("Outputted CSV for District %s optimized with %s" % (td,strat))

    if output_json:
        with open(output_json,"w") as out_file:
            # TODO make this more interesting
            o = [d.as_dict() for d in districts]
            out_file.write(json.dumps(o))


    if output_folder:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for d in districts:
            fname = os.path.join(output_folder,"%s_district.json" % d.code)
            with open(fname,"w") as out_file:
                out_file.write(json.dumps(d.as_dict()))
        fname = os.path.join(output_folder,"districts.json")
        with open(fname,"w")  as out_file:
            # output lighter version of district for district overview json
            district_list = [ d.as_dict(include_strategies=False,include_schools=False) for d in districts]
            out_file.write(json.dumps(district_list))


if __name__ == '__main__':
    cli()

