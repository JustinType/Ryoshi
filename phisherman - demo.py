import smtplib, ssl
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# construction du mail
msg = MIMEMultipart('alternative')   
sender = 'test <test@gmail.com>'
mailTo = "aoudiailian@gmail.com"
subject = "Test"

msg['From'] = sender
msg['To'] = mailTo
msg['Subject'] = subject
# mettre body à la place du texte HTML sinon
msg.attach(MIMEText("Salut !<br><br> Ceci est un mail envoyé depuis un script <u>Python</u><br>Ceci est une fausse url : <a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley'>Fake URL</a><br><br>Cordialement", 'html'))
text=msg.as_string()

# envoi du message par serveur SMTP
ssl_context = ssl.create_default_context()
s = smtplib.SMTP_SSL('test.fr', 465, context=ssl_context) # smtp.gmail.com  | webmail.ghbs.bzh 
password = getpass.getpass("Mot de passe : ")
s.login("test@test.fr", password)
s.sendmail(sender,mailTo, text)
s.quit()


# regarder : https://www.nextinpact.com/article/30341/109074-emails-avec-spf-dkim-dmarc-arcet-bimi-a-quoi-ca-sert-comment-en-profiter