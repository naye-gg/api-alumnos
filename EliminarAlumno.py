import boto3
import json

def lambda_handler(event, context):
    # Manejo flexible de entrada
    if 'body' in event:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    else:
        body = event

    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Alumno {alumno_id} eliminado correctamente',
            'response': response
        })
    }

