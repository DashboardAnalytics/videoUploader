import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmailCloud(nVideo, store, shoppingCenter, cameraIP, cameraID):
    port = 465  # For SSL
    msg = MIMEMultipart()  
    smtp_server = "smtp.gmail.com"
    sender_email = "noresponder.alaya@gmail.com"  # Enter your address
    receiver_email = "sebastian.garay.p@usach.cl"  # Enter receiver address
    password = "alayaDigitalSolutions"
    msg['Subject'] = 'Dashboard Analytics: Error con conexion a Cloud video '+str(nVideo)+' '+str(shoppingCenter)
    msg['From'] = sender_email
    msg['To'] = receiver_email

    body = 'Se ha producido un error al intentar conectar con el servidor cloud del video '+str(nVideo)+' correspondiente los siguientes datos:\nID Camara:\t'+str(cameraID)+'\nIP Camara:\t'+str(cameraIP)+'\nTienda:\t\t'+str(store)+ '\nCentro:\t\t'+str(shoppingCenter)

    msg.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def sendEmailCamera(nVideo, store, shoppingCenter, cameraIP, cameraID):
    port = 465  # For SSL
    msg = MIMEMultipart()  
    smtp_server = "smtp.gmail.com"
    sender_email = "noresponder.alaya@gmail.com"  # Enter your address
    receiver_email = "sebastian.garay.p@usach.cl"  # Enter receiver address
    password = "alayaDigitalSolutions"
    msg['Subject'] = 'Dashboard Analytics: Error con Stream video '+str(nVideo)+' '+str(shoppingCenter)
    msg['From'] = sender_email
    msg['To'] = receiver_email

    body = 'Se ha producido un error al intentar conectar con el stream del video '+str(nVideo)+' correspondiente los siguientes datos:\nID Camara:\t'+str(cameraID)+'\nIP Camara:\t'+str(cameraIP)+'\nTienda:\t\t'+str(store)+ '\nCentro:\t\t'+str(shoppingCenter)

    msg.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    

def sendEmailApi(nVideo, store, shoppingCenter, cameraIP, cameraID):
    port = 465  # For SSL
    msg = MIMEMultipart()  
    smtp_server = "smtp.gmail.com"
    sender_email = "noresponder.alaya@gmail.com"  # Enter your address
    receiver_email = "sebastian.garay.p@usach.cl"  # Enter receiver address
    password = "alayaDigitalSolutions"
    msg['Subject'] = 'Dashboard Analytics: Error con API video '+str(nVideo)+' '+str(shoppingCenter)
    msg['From'] = sender_email
    msg['To'] = receiver_email

    body = 'Se ha producido un error con la API al grabar el video '+str(nVideo)+' correspondiente los siguientes datos:\nID Camara:\t'+str(cameraID)+'\nIP Camara:\t'+str(cameraIP)+'\nTienda:\t\t'+str(store)+ '\nCentro:\t\t'+str(shoppingCenter)

    msg.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    