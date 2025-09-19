import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    AWS Lambda function para API do Pomodoro Timer
    """
    
    # Headers CORS
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        # Parse do body
        if event.get('body'):
            body = json.loads(event['body'])
        else:
            body = {}
            
        action = body.get('action', 'status')
        
        # Simular dados do timer (em produção, usar DynamoDB)
        response_data = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'status': 'success'
        }
        
        if action == 'start':
            response_data['message'] = 'Timer iniciado'
            response_data['state'] = 'work'
            response_data['duration'] = body.get('duration', 1500)  # 25 min default
            
        elif action == 'stop':
            response_data['message'] = 'Timer parado'
            response_data['state'] = 'stopped'
            
        elif action == 'status':
            response_data['message'] = 'Status do timer'
            response_data['cycles_completed'] = 0
            response_data['current_state'] = 'stopped'
            
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': str(e),
                'message': 'Erro interno do servidor'
            })
        }