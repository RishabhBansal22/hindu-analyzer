from main import main, save_results_to_pdf, save_simple_pdf
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

try:
    result = main(2)
    if result:
        try:
            path = save_results_to_pdf(result)
        except:
            path = save_simple_pdf(result)
except Exception as e:
    print(e)

def send_mail(sender=None, reciever=None, app_password=None):

    sender_email = sender if sender else os.getenv("sender_mail")
    receiver_email = reciever if reciever else os.getenv("reciever_mail")
    app_password = app_password if app_password else os.getenv("gmail_app_pass")

    msg = EmailMessage()
    msg["Subject"] = "Monthly Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Hi,\n\nPlease find attached today's 'The Hindu Editorial' PDF analysis report.\n\nBest,\nRishabh")

    # === Attach the PDF file ===
    pdf_path = path
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype="application", subtype="pdf", filename="report.pdf")

    # === Send via Gmail SMTP ===
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)

send_mail()
    

