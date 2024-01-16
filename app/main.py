from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()

# Define the templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("text_generator.html", {"request": request})

@app.get("/genai")
async def send_post_request(request: Request, name: str, message: str):
    # Get the data from the incoming request
    payload = json.dumps({
      "key": name,
      "message": message
    })
    headers = {
      'Content-Type': 'application/json'
    }
    # Define your Amazon API Gateway Endpoint
    url = <<URL-API-GATEWAY-END-POINT>>

    try:
        # Send a GET request to the external API
        response = requests.request("GET", url, headers=headers, data=payload)
        response_text = response.text
        # Check if the request was successful (HTTP status code 2xx)
        if response.ok:
            loading = False
            result = {
                'status': 'success',
                'message': 'POST request sent successfully to the external API.',
                'response_data': response.text
            }
        else:
            result = {
                'status': 'error',
                'message': f'Failed to send POST request. Status Code: {response.status_code}',
                'response_data': response.text
            }

    except Exception as e:
        result = {
            'status': 'error',
            'message': f'Exception occurred: {str(e)}'
        }
    return templates.TemplateResponse("generated_text.html", {"request": request, "result": response.text})
