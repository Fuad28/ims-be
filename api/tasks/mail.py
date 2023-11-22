from django.core.mail import BadHeaderError

import os
# from celery import shared_task
import requests
from tempfile import NamedTemporaryFile
from templated_mail.mail import BaseEmailMessage
# from api.v1.utils.logger import logger

# @shared_task
def send_email(recipients, template_name, data= {}, files= []):

    try:
        msg= BaseEmailMessage(template_name= template_name, context= data)
        if files: 
            for file_url in files: 
                msg= attach_file_to_email(msg, file_url)
        msg.send(to= recipients)

    except BadHeaderError:
        pass
        # logger(
        #     log_level= "info", next_func= "End", 
        #     source= "Send Email task: send_email", 
        #     data={"subject": data["subject"], "template_name": template_name, "data": data, "file": bool(files)})
        

def attach_file_to_email(email_obj, file_url):

    response = requests.get(file_url)
    if response.status_code == 200:
        file_name= os.path.basename(file_url)
        with NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(response.content)
            temp_file.flush()
            temp_file.seek(0)
            email_obj.attach(filename=file_name, content=temp_file.read())
            temp_file.close()
        
    return email_obj
            


