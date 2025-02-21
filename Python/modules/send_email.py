import win32com.client

def send_email(subject:str, send_to:str, body_text:str):
    outlook = win32com.client.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)

    mail.Subject =subject
    mail.to =send_to
    mail.HTMLBody = body_text
    mail.Send()
