import boto3
import botocore.config
import json
from datetime import datetime

def generata_text_using_bedrock(message:str,type_text:str) ->str:
    
    prompt_text = f"""
    \n\nHuman: Your will be acting as an copywriter for a technology company. Your goal is to 
    edit and refine this {type_text} to ensure it meets high-quality standards.
    Provide detailed feedback on grammar, punctuation, sentence structure, formatting, 
    consistency, clarity, readability, and overall coherence. 
    Additionally, assess the use of active voice, appropriate word choice, proper citation 
    and referencing, and avoid qualitive or subjective adjectives and adverbs, 
    use simple and concise words. Your suggestions should result in a polished, 
    simple and well-crafted paragraph. The text is the following: {message}.
    \n\nAssistant:
    """
    body = {
        "prompt": prompt_text,
        "max_tokens_to_sample": 2048,
        "temperature": 0.1,
        "top_k": 250,
        "top_p": 0.2,
        "stop_sequences":["\n\nHuman:"]
    }
    
    try:
        bedrock = boto3.client("bedrock-runtime", region_name="us-west-2",config = botocore.config.Config(read_timeout=300, retries = {'max_attempts':3}))
        response = bedrock.invoke_model(body=json.dumps(body),modelId="anthropic.claude-v2")
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        text = response_data["completion"].strip()

        return text
        
    except Exception as e:
        print(f"Error generating the code:{e}")
        return ""
    
def save_text_to_s3_bucket(text,s3_bucket,s3_key):
    
    s3 = boto3.client('s3')
    
    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = text)
        print("Text saved to s3")
        
    except Exception as e:
        print("Error when saving the text to s3")
        
def lambda_handler(event, context):
    event = json.loads(event['body'])
    message = event['message']
    type_text = event['key']
    print(message, type_text)
    
    generated_text = generata_text_using_bedrock(message, type_text)
    
    if generated_text:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f'text-output/{current_time}.txt'
        s3_bucket = <BUCKET-NAME>
        
        save_text_to_s3_bucket(generated_text,s3_bucket,s3_key)
        
    else:
        print("No text is generated")
    
    return {
        'statusCode': 200,
        'body': generated_text 
    }
