from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("chatbot-widget-457706-cb87129e8db6.json", scope)
# client = gspread.authorize(creds)
# sheet = client.open("Widget_Data").sheet1  

with open("/etc/secrets/GOOGLE_SHEET_CREDENTIALS") as f:
    creds_dict = json.load(f)

# Use credentials to authorize gspread
creds = Credentials.from_service_account_info(creds_dict)
client = gspread.authorize(creds)
sheet = client.open("Widget_Data").sheet1


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/user-info")
async def save_user_info(request: Request):
    try:
        data = await request.json()
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")
        phone = data.get("phone")
        age = data.get("age")

        sheet.append_row([first_name, last_name, email, phone, age])
        return {"status": "success"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        message = body.get("message")

        if not message:
            return JSONResponse(
                content={"error": "Message is required"},
                status_code=422,
                headers={"Access-Control-Allow-Origin": "*"}
            )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are Mitch Donahue, the founder and owner of Donahue Roofing & Siding in Billings, MT. ...
Speak with confidence, warmth, and professionalism — as someone who truly cares about the Billings community and delivering quality results that last."""},
                {"role": "user", "content": message}
            ]
        )

        if "choices" in response and len(response["choices"]) > 0:
            reply = response["choices"][0]["message"]["content"]
            return JSONResponse(
                content={"reply": reply},
                headers={"Access-Control-Allow-Origin": "*"}
            )
        else:
            return JSONResponse(
                content={"error": "No reply found"},
                status_code=500,
                headers={"Access-Control-Allow-Origin": "*"}
            )

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500,
            headers={"Access-Control-Allow-Origin": "*"}
        )
