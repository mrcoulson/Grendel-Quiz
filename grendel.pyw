from Tkinter import *
import random
import datetime
import smtplib
import tkMessageBox
from email.mime.text import MIMEText


class Application(Frame):

    intScore = -1
    dtNow = datetime.datetime.now()
    strTestString = "BEOWULF"
    strWrongAnswer = ["Try again!", "Nope!", "Don't give up!", "Bzzz!", "The answer is 'Beowulf'!"]

    def createWidgets(self):
    
        def callback():
            strUserInput = self.ANSWER.get()
            strUpperInput = strUserInput.upper()
            if strUpperInput != self.strTestString:
                # self.RESULT["text"] = random.choice(strWrongAnswer)
                self.intScore += 1
                if self.intScore <= 3:
                    self.RESULT["text"] = self.strWrongAnswer[self.intScore]
                else:
                    self.RESULT["text"] = self.strWrongAnswer[4]
                    self.SUBMIT.configure(state=DISABLED, background="#CCCCCC")
                    self.QUIT.configure(background="#72c337")
            else:
                self.RESULT["text"] = "Good answer!"
                self.SUBMIT.configure(state=DISABLED, background="#CCCCCC")
                self.QUIT.configure(background="#72c337")
                
        def submitAndQuit():
            f = open("C:\grendel_scores.txt","a")
            strS = str(self.intScore)
            strD = str(self.dtNow)
            f.write(strD + "\t" + strS + "\n")
            f.flush()
            f.close()
            self.quit()
            sendEmail()

        # Create an email function.
        def sendEmail():
            # Set a variable for sender.
            strFrom = "you@whatever.com"
            # Set a variable for recipients. Multiple recipients are handled with an array.
            strTo = ["someaddress@isp.com", "another@another.com", "itsanarray@indeed.com"]
            # Set variables for username and password for SMTP authentication.
            strUser = "username"
            strPass = "secret_password"
            # Set variables for the score and current timestamp.
            strS = str(self.intScore)
            strD = str(self.dtNow)
            # Build the message. The "\n" character makes a new line. MIMEText works with the colons.
            strMessage = "Timestamp: " + strD + "\n" + "Score: " + strS
            strMessageToSend = MIMEText(strMessage)
            # Try to send the email.
            try:
                # Create an instance of the smtplib called smtpObj using the host and port specified.
                smtpObj = smtplib.SMTP("smtp.whatever.com", 25)
                # Say hi to the server.
                smtpObj.ehlo()
                # Start SMTP encryption.  I don't know if this is totally necessary.
                smtpObj.starttls() #This stopped working for some reason. Still sends emails, though. 
                # Say hi again because Python documentation says to do so.
                # smtpObj.ehlo()
                # Authenticate with username and password from above.
                smtpObj.login(strUser, strPass)
                # Send the email.
                smtpObj.sendmail(strFrom, strTo, strMessageToSend.as_string())
            # Catch an exception.
            except Exception as exc:
                # Show that there was an error.
                tkMessageBox.showerror("Error", exc)


        self.ASK = Label(self, text="Who defeated Grendel?")
        self.ASK.pack()

        self.ANSWER = Entry(self)
        self.ANSWER.pack()

        self.RESULT = Label(self)
        self.RESULT.pack()

        self.SUBMIT = Button(self, text="SUBMIT", command=callback, background="#72c337")
        self.SUBMIT.pack({"side": "left"})

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["background"] = "#ea5959"
        self.QUIT["command"] = submitAndQuit
        self.QUIT.pack({"side": "right"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
root.minsize(width=250, height=100)
root.geometry('250x100')
root.maxsize(width=250, height=100)
app = Application(master=root)
app.mainloop()
root.destroy()
        
