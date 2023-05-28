import os
import json
import boto3

is_lambda = bool(os.environ.get("LAMBDA_TASK_ROOT", False))

def handler(event, context):
    print("[INPUT]", type(event), event)
    if is_lambda:
        if type(event) is str:
            event = json.loads(event)
        if "body" in event:
            # in apigateway
            body = json.loads(event['body'])
        else:
            # in pure lambda
            body = event
    else:
        # excuted locally
        body = event

    # invoke lambda
    lambda_client = boto3.client('lambda')
    payload = json.dumps(body, ensure_ascii=False).encode()
    # TODO: 태그를 통해 해당 람다 함수의 arn 을 가져오게끔 리팩토링
    lambda_arn = "arn:aws:lambda:ap-northeast-2:521049726185:function:playwright-dev"
    response = lambda_client.invoke(
        FunctionName=lambda_arn,
        InvocationType='RequestResponse',
        Payload=payload,
    )
    # invoke result
    ret = json.loads(response['Payload'].read())
    print("[RESPONSE]", ret)
    status_code = ret["statusCode"]

    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(ret, ensure_ascii=False)
    }