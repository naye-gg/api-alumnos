import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("EVENT: " + json.dumps(event))

    # Obtener parámetros desde query o body
    params = {}
    if 'queryStringParameters' in event and event['queryStringParameters']:
        params = event['queryStringParameters']
    elif 'body' in event:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        params = body

    tenant_id = params.get('tenant_id')
    alumno_id = params.get('alumno_id')

    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Faltan parámetros tenant_id o alumno_id'})
        }

    # Consulta en DynamoDB
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
            'body': json.dumps({'error': f'Error al consultar DynamoDB: {str(e)}'})
        }

    item = response.get('Item')
    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Alumno no encontrado'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

