import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("EVENT: " + json.dumps(event))
    
    params = event.get('queryStringParameters') or {}
    tenant_id = params.get('tenant_id')
    alumno_id = params.get('alumno_id')

    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'body': 'Faltan parámetros tenant_id o alumno_id'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    try:
        response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al consultar DynamoDB: {str(e)}'
        }

    item = response.get('Item')
    if not item:
        return {
            'statusCode': 404,
            'body': 'Alumno no encontrado'
        }

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

