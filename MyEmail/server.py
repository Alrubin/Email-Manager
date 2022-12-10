import smtplib
import getpass
import email
import sys

#########################################################################################
# SERVER CLASS
#########################################################################################

class MyEmailServer:
    
    #--------------------------------------------------------
    def __init__(self, sender, localhost, port):
        self.sender = sender
        self.localhost = localhost
        self.port = port
        
        #consistency check
        if not isinstance(port, int):
            raise TypeError("The variable 'port' is assumed to be an integer")
        
    #--------------------------------------------------------
    def __str__(self):
        return f"The email server for this account: {self.sender}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.sender}, {self.localhost}, {self.port})"
    
    #--------------------------------------------------------
       
    def _send(self,message):
        """ function to send the message """
        
        #consistency check
        if not isinstance(message, email.message.EmailMessage):
            raise TypeError("The variable is assumed to be an email.message.EmailMessage() object")
       
            
        everything_is_ok  = True 
        password = getpass.getpass('Password: ')

        #connect to the email server
        if everything_is_ok:
            try:
                mail_server = smtplib.SMTP(self.localhost, self.port)
            except:
                print("Connection Failed - Check Server Permissions (localhost/port/auth)")
                everything_is_ok  = False

            
        #login into the email server
        if everything_is_ok:
            try:            
                mail_server.ehlo()
                mail_server.starttls()
                mail_server.login(self.sender, password)
            except:
                print("Login Failed - Check Password")
                everything_is_ok  = False
            
        #Send the message
        if everything_is_ok:
            try:            
                mail_server.send_message(message)
                #stop the connection
                mail_server.quit()
                print("Successfully sent email")
            except:
                print("Sending Failed - Check Destination Email and/or CC Format")
            
     