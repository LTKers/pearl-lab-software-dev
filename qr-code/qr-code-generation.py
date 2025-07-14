import qrcode
import cv2 as cv
from qrcode.image.pure import PyPNGImage

#QRCode creation class
qr=qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_H, box_size=10, border=4)

#Creates QRCode image using input and saves into images directory
block_name=input("Enter block name")
qr.add_data(block_name)
img = qr.make_image(image_factory=qrcode.image.pure.PyPNGImage, fill_color="black", back_color="white")
imgsave=img.save(f'QR_Images/{block_name}.png')