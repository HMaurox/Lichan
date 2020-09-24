import smtplib

envia="usbblockchain@gmail.com"
recibe="homerux.007@gmail.com"
passw="sanbuenventura"
mensaje = "Enviado desde python"

#server#
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls
server.login(envia,passw)
print("accedio a cuenta")
server.sendmail(envia,recibe,mensaje)
print("email enviado a:", recibe)

