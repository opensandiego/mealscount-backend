import csv,sys,os.path

# CSV Provided by CFPA 
cfpa_snp_report_csv = csv.DictReader(open(sys.argv[1]))

# Month we are filtering for
claim_date = '2019-04-01'

# Latest CALPADS with modified column names
latest_csv = csv.DictReader(open("latest.csv"))

served = {}
output_cols = []
for row in cfpa_snp_report_csv:
    cds_code = row['CDSCode']
    if row["ClaimDate"] != claim_date: continue
    if not cds_code:
        #print("%(SiteName)s %(CustomerName)s does not have a CDS Code" % row)
        continue
    county = int(cds_code[:2])
    district = int(cds_code[2:7])
    school = int(cds_code[7:])

    k = (county,district,school)

    # Are the mls served daily?
    bkfst_severe_served = int(row["MlsServedSiteBreakfastSevereNeedTotal"] or 0)
    bkfst_trad_served = int(row["MlsServedSiteBreakfastTraditionalTotal"] or 0) 
    bkfst_severe_days = float(row["DaysServedQtySiteBreakfastSevereNeed"] or 0)
    bkfst_trad_days = float(row["DaysServedQtySiteBreakfastTraditional"] or 0)
    bkfst_daily = int((bkfst_severe_days and bkfst_severe_served/bkfst_severe_days or 0) + \
                  (bkfst_trad_days and bkfst_trad_served/bkfst_trad_days or 0))

    lunch_served = int(row["MlsServedSiteLunchTotal"] or 0)
    lunch_days = float(row["DaysServedQtySiteLunch"] or 0)
    lunch_daily = int(lunch_days and lunch_served/lunch_days or 0)

    served[k] = {
        "daily_breakfast_served": bkfst_daily,
        "daily_lunch_served": lunch_daily,
    }
    if len(served) == 1:
        output_cols.extend(served[k].keys())


schools = {}
missing,updated = 0,0

for row in latest_csv:
    county = int(row["County Code"])
    district = int(row["District Code"])
    school = int(row["School Code"])
    k = (county,district,school)
    schools[k] = row

    # Tweak for CAlifornia
    row["include_in_mealscount"] = "(Public)" in row["School Type"] 

    if not k in served:
        #print("Missing Served for %(District Name)s / %(School Name)s - %(County Code)s %(District Code)s %(School Code)s %(School Type)s" % row)
        schools[k]["daily_breakfast_served"] = "" 
        schools[k]["daily_lunch_served"] = "" 
        missing += 1
    else:
        schools[k].update(served[k])
        updated += 1
    if len(schools) == 1:
        output_cols.extend(row.keys())

output_cols = set(output_cols)
print("%i meals served schools, %i calpads upc schools, %i not matched, %i updated" % (len(served),len(schools),missing,updated) )

if len(sys.argv) >= 2 and not os.path.exists(sys.argv[2]):
    with open(sys.argv[2],"w") as f:
        print("Writing merged data to updated_latest.csv")
        writer = csv.DictWriter( f,fieldnames = output_cols )
        writer.writeheader()
        for k in schools:
            writer.writerow(schools[k])
else:
    print("please specify output csv filename as second arg, and verify it does not already exist")
