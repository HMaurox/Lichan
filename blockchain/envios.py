import yagmail
import smtplib
correo = yagmail.SMTP("usbblockchain@gmail.com","sanbuenventura")
correo.send(
    to="felipeidrobo10@gmail.com",
    subject="Envio de claves dinamica -TEST",
    contents="su clave dinamica es 534w687r9fco",
)

