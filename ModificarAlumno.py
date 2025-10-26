import boto3
import json

def lambda_handler(event, context):
    # Manejo flexible de entrada (por body o directa)
    if 'body' in event:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    else:
        body = event

    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']
    alumno_datos = body['alumno_datos']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        UpdateExpression="set alumno_datos=:alumno_datos",
        ExpressionAttributeValues={
            ':alumno_datos': alumno_datos
        },
        ReturnValues="UPDATED_NEW"
    )

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json; charset=utf-8"
        },
        # 👇 Esto permite que Postman muestre acentos y ñ correctamente
        'body': json.dumps({
            'message': 'Alumno actualizado correctamente',
            'updated': response.get('Attributes', {})
        }, ensure_ascii=False)
    }

