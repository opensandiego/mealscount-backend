import csv,argparse,us.states,os,os.path,re

COL_MAP = [
    "state",
    "District Code",
    "District Name",
    "School Code",
    "School Name",
    "individual_isp",
    "proxy_isp",
    "claiming_isp",
    "participating_in_cep",
    "total_enrolled",
]


def parse_file(csv_filename):
    with open(csv_filename,'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = []
        cols = None

        for row in reader:
            if not cols:
                cols = row
                continue

            # Determine State
            # Determine 
            school = dict(zip(
                COL_MAP,
                row
            )) 
            try:
                school['total_enrolled'] = int(school['total_enrolled'])
                school['total_eligible'] = round(float(school['individual_isp'].replace('%',''))/100 * school['total_enrolled'])
            except ValueError: 
                school['total_eligible'] = ''

            try:
                school['state'] = us.states.lookup(school['state'].strip()).abbr.lower()
            except AttributeError:
                print("Could not find state",school['state'])
            rows.append(school)

        print( rows[0] )
        return rows

def write_schools(rows):
    states = {}
    for school in rows:
        states.setdefault(school['state'],[])
        states[school['state']].append(school)

    for state in states:
        if not os.path.exists(state):
            os.mkdir(state)
        print("Writing ",state.upper())
        with open(os.path.join(state,"latest.csv"),'w') as csv_out:
            latest = csv.DictWriter(csv_out,fieldnames=rows[0].keys())
            latest.writeheader()
            school_codes = {} # We need to ensure this is unique!
            district_codes = {}
            for school in states[state]:
                code = school['School Code'] or "Unknown"
                if code in school_codes:
                    i = school_codes[code]
                    school_codes[code] = i + 1
                    school['School Code'] = '%s-%i' % (code,i)
                else:
                    school_codes.setdefault(code,0)

                # Also we have to ensure all district names / code pairs are unique
                # (there are duplicate codes for different names in the source file from frac)
                if school['District Code'].strip() == '':
                    school['District Code'] = re.sub(r'[^a-z0-9_\-]+','-',school['District Name'].lower())
                if school['District Code'] in district_codes and \
                   school['District Name'] !=  district_codes[school['District Code']]:
                    school['District Name'] = district_codes[school['District Code']]
                else:
                    district_codes.setdefault(school['District Code'], school['District Name'])
                latest.writerow(school)

    # TODO
    # create folder for each state if it doesn't exist
    # write out CSV data file for each state
    # District Name,District Code,School Name,School Code,total_enrolled,total_eligibleA
    # optional: daily_breakfast_served, daily_lunch_served
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''
        Process CEP Database from https://frac.org/research/resource-library/community-eligibility-cep-database
        to generate individual datasets for each state for MealsCount
        '''
    )
    parser.add_argument('csv_file', type=str, nargs=1,
                    help='The CSV Filename')

    parser.add_argument('--write', dest='write', action='store_true',
                    help='To actually write the data, use this option')

    args = parser.parse_args()

    rows = parse_file(args.csv_file[0]) 
    print("Found %i schools" % len(rows))

    districts = {}
    for s in rows:
        districts.setdefault(s['District Code'],0)
        districts[s['District Code']] += 1
    print("%i of %i districts over 12 schools" % (len([d for d in districts.values() if d > 12]),len(districts)))

    print("\t%i with enrollment data" %  len([s for s in rows if s['total_enrolled']]))
    print("\t%i with isp data" %  len([s for s in rows if s['total_eligible']]))

    if args.write:
        write_schools(rows)
    else:
        print("Use --write to write out %i schools" % len(rows))
