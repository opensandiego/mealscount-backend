# AWS Lambda Handler
#
# Use Dockerfile.lambda to package/upload (see the instructions in the Dockerfile)
# 
from strategies.base import CEPDistrict,CEPSchool
from cep_estimatory import add_strategies
import os,datetime,json,time
import zipfile
from io import BytesIO
import base64
import sys

import boto3,botocore

#print("## ENV ## ",os.environ)
if "SENTRY_DSN" in os.environ:
    import sentry_sdk
    from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
    #print("initializing sentry dsn with ",os.environ["SENTRY_DSN"])
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        integrations=[AwsLambdaIntegration(timeout_warning=True)]
    )

def lambda_handler(event, context, local_output=False):
    print(boto3.__version__)
    print(botocore.__version__)

    # Receives JSON district as input (same as server.py api endpoint)
    d_obj = event
    if "zipped" in event:
        print("Decompressing", len(event["zipped"]))
        with BytesIO(base64.b64decode(event["zipped"])) as df:
            with zipfile.ZipFile(df) as eventzip:
                d_obj = json.loads(eventzip.open("data.json").read())

    key = d_obj["key"]

    max_groups,evaluate_by = int(d_obj.get("max_groups",10)),d_obj.get("evaluate_by","reimbursement")
    schools = d_obj["schools"]
    district = CEPDistrict(d_obj["name"],d_obj["code"],state=d_obj["state_code"])

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

    strategies = d_obj.get("strategies_to_run",["Pairs","OneToOne","Exhaustive?evaluate_by=%s"% evaluate_by,"OneGroup","Spread","Binning","NYCMODA?fresh_starts=50&iterations=1000&ngroups=%s&evaluate_by=%s" % (max_groups,evaluate_by),"GreedyLP"])
    add_strategies(
        district,
        *strategies
    )

    t0 = time.time()
    district.run_strategies()
    district.evaluate_strategies(max_groups=max_groups,evaluate_by=evaluate_by)

    result = district.as_dict()
    result["state_code"] = state
    result["max_groups"] = max_groups
    result["evaluate_by"] = evaluate_by
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

def test_run(event,n):
        event["key"] = "test/%i/%02i/%02i/%02i%02i%02i-%s.json" % (
            n.year,n.month,n.day,n.hour,n.minute,n.second,event["code"]
        )
        event["state_code"] = "test"
        class TestContext(object):
            env = {}

        if "--zip_test" in sys.argv:
            with BytesIO() as mf:
                with zipfile.ZipFile(mf,mode='w',compression=zipfile.ZIP_BZIP2) as zf:
                    zf.writestr('data.json', json.dumps(event))
                event = {"zipped": base64.b64encode(mf.getvalue()) }

        return lambda_handler(event,TestContext(),local_output="AWS_ACCESS_KEY_ID" not in os.environ)

if __name__ == "__main__":
    # For Local Testing
    n = datetime.datetime.now()
    with open(sys.argv[1]) as f:
        event = json.loads(f.read())
        test_run(event,n)

