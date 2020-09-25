import yagmail
import smtplib
correo = yagmail.SMTP("usbblockchain@gmail.com","sanbuenventura")
correo.send(
    to="vlatruo@gmail.com",
    subject="Envio de claves dinamica -TEST",
    contents=[ "Esta es su clave dinámica de acceso temporal, bienvenido a LICHAIN : ",'temp_cd.jpg']
)

