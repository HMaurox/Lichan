from PIL import Image, ImageDraw, ImageFont

image = Image.open("clave_dina.jpg")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", 44)
draw.text((660,380), "6AB7 D17D", font=font, fill="Black")
image.save("temp_cd.jpg")
