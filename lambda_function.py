# AWS Lambda Handler
#
# Use Dockerfile.lambda to package/upload (see the instructions in the Dockerfile)
# 
from strategies.base import CEPDistrict,CEPSchool
from cep_estimatory import add_strategies
import os,datetime,json,time

import boto3,botocore

def lambda_handler(event, context, local_output=False):
    print(boto3.__version__)
    print(botocore.__version__)

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

    strategies = d_obj.get("strategies_to_run",["Pairs","OneToOne","Exhaustive","OneGroup","Spread","Binning","NYCMODA?fresh_starts=10&iterations=150"])
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
    result_key = key

    if local_output:
        print( "Would output to s3bucket:%s" % result_key )
        print( json.dumps(result,indent=1) )
    else:
        s3_client = boto3.client('s3')

        s3_client.put_object( 
            Body = json.dumps(result), 
            Bucket=os.environ.get("S3_RESULTS_BUCKET","mealscount-results"), 
            Key=result_key, 
            ContentType="application/json",
            ACL='public-read',
        )

if __name__ == "__main__":
    # For Local Testing
    import sys
    n = datetime.datetime.now()
    with open(sys.argv[1]) as f:
        event = json.loads(f.read())
        event["key"] = "test/%i/%02i/%02i/%02i%02i%02i-%s.json" % (
            n.year,n.month,n.day,n.hour,n.minute,n.second,event["code"]
        )
        event["state_code"] = "test"
        class TestContext(object):
            env = {}
        lambda_handler(event,TestContext(),local_output="AWS_ACCESS_KEY_ID" not in os.environ)
