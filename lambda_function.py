# AWS Lambda Handler
#
# To Package:
# Per https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-venv
# This is best done in a clean folder with only the base_requirements.txt installed (not requirements.txt) 
#
# > virtualenv venv 
# > source venv/bin/activate
# > pip install -r base_requirements.txt
# > deactivate
# > OLDPWD=`pwd`
# > zip -g function.zip  -r ./strategies
# > cd venv/lib/python3.8/site-packages/
# > zip -r9 ${OLDPWD}/function.zip .
# > cd ${OLDPWD} 
# > zip -rg function.zip *.py strategies
#
# Then upload the function!
# 
from strategies.base import CEPDistrict,CEPSchool
from cep_estimatory import add_strategies
import os,datetime,json,time

# Assumed to come in with S3
try:
    import boto
except ImportError:
    print("No boto installed, cannot upload to S3")

def lambda_handler(event, context, local_output=False):
    # Receives JSON district as input (same as server.py api endpoint)
    d_obj = event
    key = d_obj["key"]

    schools = d_obj["schools"]
    district = CEPDistrict(d_obj["name"],d_obj["code"],reimbursement_rates=d_obj["rates"])

    state = d_obj["state_code"]

    i = 1 
    for row in schools:
        # Expecting { school_code: {active, daily_breakfast_served,daily_lunch_served,total_eligible,total_enrolled }}
        if not row.get("school_code",None) or not row.get("total_enrolled",None):
            continue
        row["School Name"] = row.get("school_name","School %i"%i)
        row["School Code"] = row.get("school_code","school-%i"%i)
        row["School Type"] = row.get("school_type","")
        row['include_in_mealscount'] = row.get('active','true') and 'true' or 'false'
        i += 1
        district.add_school(CEPSchool(row))

    strategies = d_obj.get("strategies",["Pairs","OneToOne","Exhaustive","OneGroup","Spread","Binning","NYCMODA?fresh_starts=10&iterations=150"])
    add_strategies(
        district,
        *strategies
    )

    t0 = time.time()
    district.run_strategies()
    district.evaluate_strategies()

    result = district.as_dict()
    result["state_code"] = state
    result["optimization_info"] = {
        "timestamp":str(datetime.datetime.now()),
        "time": time.time() - t0
    }

    # Posts resulting data to S3 
    # with "key"
    n = datetime.datetime.now()
    result_key = "/data/%i/%02i/%02i/%s-%s.json" % (n.year,n.month,n.day,d_obj["code"],key)

    if local_output:
        print( "Would output to s3bucket:%s" % result_key )
        print( json.dumps(result,indent=1) )
    else:
        s3_client = boto3.client('s3')

        s3_client.put_object( 
            Body = json.dumps(result), 
            Bucket=context.env.get("S3_RESULTS_BUCKET","mealscount-results"), 
            Key=result_key, 
            ContentType="application/json",
            ACL='public-read',
        )

if __name__ == "__main__":
    # For Local Testing
    import sys
    with open(sys.argv[1]) as f:
        event = json.loads(f.read())
        event["key"] = "xxxTESTKEYHASHxxx"
        event["state_code"] = "test"
        class TestContext(object):
            env = {}
        lambda_handler(event,TestContext(),local_output=True)
