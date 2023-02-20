import csv,codecs,time
from multiprocessing import Pool, cpu_count, freeze_support
from re import I
import click
from strategies.base import CEPDistrict,CEPSchool
from strategies.naive import CustomGroupsCEPStrategy,OneGroupCEPStrategy,OneToOneCEPStrategy
from cep_estimatory import add_strategies
import sys

STRATEGIES = [
  "Pairs",
  "OneToOne",
  "Exhaustive",
  "OneGroup",
  "Spread",
  #"Binning",
  "GreedyLP",
  "NYCMODA?fresh_starts=50&iterations=1000&ngroups=%(ngroups)s",
]

@click.command()
@click.option("--csv-file",default=None,help="CSV File in MealsCount format")
@click.option("--state",default=None,help="State Abbrev (e.g. CA, NY)")
@click.option("--csv-encoding",default="utf-8",help="CSV Encoding (e.g. utf-8, latin1)")
@click.option("--debug",is_flag=True,help="Run a quick test run on districts of < 5 schools just to test")
@click.option("--max-groups",default=10,help="Paramter for max groups limiter on monte carlo")
@click.option("--output-file",default=None,help="output file (default is ./statewide-XX-output.csv)")
def run(csv_file,state,csv_encoding,debug,max_groups,output_file):
  # Load
  districts,schools,lastyear_groupings = load_from_csv(csv_file,csv_encoding,state)

  # Summary Import Stats
  #print("Processed %i schools from %s into %i districts" % (len(schools),state,len(districts)))
  #print("%i schools with ADP > 100%%" % len([s 
  #  for s in schools if s.bfast_served > s.total_enrolled or s.lunch_served > s.total_enrolled
  #]))

  if debug:
    #print("Trimming districts for debug run")
    districts = {c:d for c,d in districts.items() if len(d.schools) <= 5}

  # Optimize with max reimbursement
  strategies = [s%{"ngroups":max_groups} for s in STRATEGIES]
  results = optimize(districts,strategies)
  # Optimize with max coverage
  results_coverage = optimize(districts,strategies,goal="coverage")

  # Run Naive Baselines
  for d in districts.values():
    d.strategies.append(OneGroupCEPStrategy())
    d.strategies.append(OneToOneCEPStrategy())
    lastyear = CustomGroupsCEPStrategy()
    lastyear.set_groups([(x[1],x[2]) for x in lastyear_groupings if x[0] == d.code])
    d.strategies.append(lastyear)
    d.run_strategies()

  #import code; code.interact(local=locals())

  # Summary Results
  # Total Change from baseline
  district_results = {}
  for r in results:
    district_results[r["code"]] = {"reimb": r["reimb"],"best_reimb":r["best"]}
  for r in results_coverage:
    #district_results[r["code"]]["coverage"] = r["coverage"]
    district_results[r["code"]]["best_coverage"] = r["best"]
  for d in districts.values():
    district_results[d.code]["onegroup_reimb"] = d.strategies[0].reimbursement
    district_results[d.code]["onetoone_reimb"] = d.strategies[1].reimbursement
    district_results[d.code]["lastyear_reimb"] = d.strategies[2].reimbursement
    district_results[d.code]["onegroup_coverage"] = d.strategies[0].students_covered
    district_results[d.code]["onetoone_coverage"] = d.strategies[1].students_covered
    district_results[d.code]["lastyear_coverage"] = d.strategies[2].students_covered

  def deltapercent(x,y,explain):
    if y == 0 and x > 0: return "100%"
    elif y == 0 and x == 0: return "0%"
    diff = (((x-y)/y)*100.0)
    return "%0.1f%% %s %s" % (diff,diff>0 and "increase" or "decrease",explain)

  baseline_reimb = max(sum([d["onegroup_reimb"] for d in district_results.values()]),sum([d["onegroup_reimb"] for d in district_results.values()]))
  #print("Naive Baseline:",baseline_reimb)
  lastyear_reimb = sum([d["lastyear_reimb"] for d in district_results.values()])
  #print("Last Year:",lastyear_reimb,deltapercent(lastyear_reimb,baseline_reimb,"over baseline"))
  mc_reimb = sum([d["reimb"] for d in district_results.values()])
  #print("MealsCount:",mc_reimb,deltapercent(mc_reimb,lastyear_reimb,"over last year"),deltapercent(mc_reimb,baseline_reimb,"over baseline"))

  # Output Groupings
  output(districts,results,results_coverage,state,lastyear_groupings,output_file=output_file)

def output(districts,results,results_coverage,state,lastyear_groupings,output_file):
  fname = output_file or "statewide-%s-output.csv" % state
  #print("Writing results to %s" % fname)
  with open(fname,"w") as f:
    writer = csv.writer(f)
    writer.writerow((
      "district_code",
      "district_name",
      "school_code",
      "school_name",
      "total_enrolled",
      "total_eligible",
      "daily_breakfast_served",
      "daily_lunch_served",
      "free_bfast_rate",
      "paid_bfast_rate",
      "free_lunch_rate",
      "paid_lunch_rate",
      "onegroup_reimbursement",
      "onetoone_reimbursement",
      "lastyear_reimbursement",
      "mealscount_reimbursement",
      "mealscount_coverage",
      "mc_coverage_reimbursement",
      "mc_coverage_coverage",
      "lastyear_grouping",
      "mealscount_grouping",
      "coverage_grouping",
    ))
    for d in districts.values():
      school_results = [r for r in results if r["code"] == d.code][0]["schools"]
      cov_school_results = [r for r in results_coverage if r["code"] == d.code][0]["schools"]
      for s in d.schools:
        lastyear_group = [g[1] for g in lastyear_groupings if g[2] == s.code and g[0] == d.code]
        if lastyear_group: lastyear_group = lastyear_group[0]
        else: lastyear_group = ""
        sr = [sr for sr in school_results if sr["school_code"] == s.code][0]
        csr = [sr for sr in cov_school_results if sr["school_code"] == s.code][0]
        writer.writerow((
          d.code,
          d.name,
          s.code,
          s.name,
          s.total_enrolled,
          s.total_eligible,
          s.bfast_served,
          s.lunch_served,
          sr["rates"]["free_bfast"],
          sr["rates"]["paid_bfast"],
          sr["rates"]["free_lunch"],
          sr["rates"]["paid_lunch"],
          d.strategies[0].school_reimbursement(s),
          d.strategies[1].school_reimbursement(s),
          d.strategies[2].school_reimbursement(s),
          sr["reimbursement"],
          sr["coverage"],
          csr["reimbursement"],
          csr["coverage"],
          lastyear_group,
          sr["grouping"],
          csr["grouping"],
        ))

def load_from_csv(csv_file,csv_encoding,state):
  districts = {}
  schools = []
  lastyear_groupings = []
  for row in csv.DictReader(open(csv_file,encoding=csv_encoding)):
    school = CEPSchool(row)
    schools.append(school)
    if "cep_grouping" in row and row["cep_grouping"].strip():
      lastyear_groupings.append((row["district_code"],row["cep_grouping"],row["school_code"]))

    if row["district_code"] not in districts:
        districts[row["district_code"]] = CEPDistrict(row["district_name"],row["district_code"],state)
    if school.total_enrolled > 0:
        districts[row["district_code"]].add_school(school)
  return districts,schools,lastyear_groupings

def optimize(districts,strategies,goal="reimbursement"):
  # Optimize with standard Strategies
  #print("optimizing with %s" % (','.join(strategies)))
  district_map = dict([(d.code,d) for d in districts.values()])
  t0 = time.time()
  # We use multiprocessing to speed this all up
  PROCESSES = cpu_count() - 1

  count = sum([len(d.schools) for d in districts.values()])
  class Progress(object):
    processed = 0
    def update(self,n):
      self.processed += n
      sys.stdout.write("%0.4f\n"%(float(self.processed)/count))
      sys.stdout.flush()
  
  #with click.progressbar(length=count,label='Running Strategies on Districts') as bar:
  #with Progress() as progress:
  progress = Progress()
  with Pool(PROCESSES) as pool:
      results = [pool.apply_async(mp_processor, (d,goal,strategies)) for d in districts.values()]
      for r in results:
          result = r.get()
          _d = district_map[result["code"]]
          #bar.update(len(_d.schools))
          progress.update(len(_d.schools))
  total_time = time.time() - t0
  #print("Optimized in %0.1fs" % total_time)
  return [r.get() for r in results]
 
def mp_processor(district,goal,strategies):
  add_strategies(district,*strategies)
  district.run_strategies()
  district.evaluate_strategies(evaluate_by=goal)
  schools = []
  gname = 1
  for g in district.best_strategy.groups:
    for s in g.schools:
      reimb = g.school_reimbursement(s)
      s.set_rates(district)
      schools.append({
        "school_code":s.code,
        "rates":s.rates.as_dict(),
        "district_code":district.code,
        "reimbursement": reimb,
        "coverage": g.cep_eligible and s.total_enrolled or 0,
        "grouping": g.cep_eligible and "G%i" % gname or "Not CEP Eligible",
      })
    if g.cep_eligible:
      gname += 1
  
  return {
      "code":district.code,
      "reimb":district.best_strategy.reimbursement,
      "best":district.best_strategy.name,
      "groupings": [g.as_dict() for g in district.best_strategy.groups],
      "schools": schools,
  }

 
if __name__ == '__main__':
    # https://docs.python.org/3.7/library/multiprocessing.html?highlight=process#multiprocessing.freeze_support
    freeze_support()
    run()

