import boto3

def lambda_handler(event, context):
    tenant_id = event['queryStringParameters']['tenant_id']
    alumno_id = event['pathParameters']['alumno_id']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )

    return {
        'statusCode': 200,
        'response': response
    }

