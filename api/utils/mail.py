from rest_framework.exceptions import APIException

from api.tasks.mail import send_email as send_email_task

def send_mail(subject= None, recipients= None, template_name= None, data= {}, files= []):
    if not (subject and recipients and template_name):
        raise APIException("subject, recipients and template_name are required.")

    files= files if isinstance(files, list) else [files]
    all_strings = all(isinstance(item, str) for item in files)
    if not all_strings:
        raise APIException("files should be in url string format.")

    if not (isinstance(template_name, str) and isinstance(subject, str)):
        raise APIException("subject, template_name are strings.")
    
    recipients= recipients if isinstance(recipients, list) else [recipients]
    data["subject"]= subject

    send_email_task(recipients, template_name, data, files)
    # send_email_task.delay(recipients, template_name, data, files)
