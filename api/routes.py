from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# origins = [
#     "http://localhost:3000",  # Your frontend running on localhost:3000
#     "http://127.0.0.1:3000/frontend/index.html?serverWindowId=c611d471-c574-41bc-8a97-45f159d05eca" # Specific IP address and port
# ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allows all headers in the request
    )

class LeadCapture(BaseModel):
    email : str


@app.post("/download_mail/")
def capture_mail(mail:LeadCapture):
    print(mail.email)
    return {
        "message":f"email {mail.email} recieved successfully"
    }


@app.get("/health")
def health_Chk():
    
    return {
        "status":f"{status.HTTP_200_OK}"
    }
