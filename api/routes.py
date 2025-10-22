from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class LeadCapture(BaseModel):
    email : str


@app.post("/download_mail/")
def capture_mail(mail:LeadCapture):
    return mail


@app.get("/health")
def health_Chk():
    return {
        "status":f"{status.HTTP_200_OK}"
    }
