import email
import mimetypes
import os
from .server import MyEmailServer

#########################################################################################

class MyEmailMessage:
    
    set_server = None
    
    #--------------------------------------------------------
    def __init__(self, subject, body):  
        
        self.subj = subject
        self.body = body
        self.attachments = []

        self.message = email.message.EmailMessage()
        self.message["Subject"] = subject
        self.message.set_content(body)
        self.message["From"] = self.set_server.sender
        
    #--------------------------------------------------------
    def __str__(self):
        message = f'''Subject: {self.subj}
                    \nAttachments: {self.attachments}
                   \n%---------------------------------------%
                   \n{self.body}
        '''
        
        return message
    
    def __repr__(self):
        return f"{self.__class__.__name__}(\'{self.message['Subject']}\')"
    
    #--------------------------------------------------------
    def add_attachment(self, path):
        self.attachments.append(path)
        attachment_filename = os.path.basename(path)
        mime_type, _ = mimetypes.guess_type(path)
        mime_type, mime_subtype = mime_type.split('/', 1)

        with open(path, 'rb') as ap:
            self.message.add_attachment(ap.read(),
                              maintype=mime_type,
                              subtype=mime_subtype,
                              filename=attachment_filename)
            
    #--------------------------------------------------------    
    def send_to(self,target, cc = None):
        
        #reset recipient (if any) and update it
        del self.message["To"]
        self.message["To"] = target
        
        # check cc type
        if cc is not None:
            if not isinstance(cc, list):
                raise TypeError("CC must be a list")
            del self.message["cc"] #remove possible previous cc elements
            self.message["cc"] = ",".join(cc)
        self.set_server._send(self.message)
            
                
    #--------------------------------------------------------    
    def update_subject(self, new_subject):
        del  self.message["Subject"]
        self.message["Subject"] = new_subject