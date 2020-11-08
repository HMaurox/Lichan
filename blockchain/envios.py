import yagmail
import smtplib
import os

temporal = "blockchain/temporal"+".pdf"
correo = yagmail.SMTP("usbblockchain@gmail.com","sanbuenventura") # Datos de acceso al correo del proyecto
correo.send(
    to= CORREO,
    subject= "Certificado Usuario- LICHAIN",
    contents=["Lichain, hace entrega de la solicitud de cerificado de Usuario: ",temporal]
    )
os.remove(temporal)    
print("su correo fue enviado correctamente")

