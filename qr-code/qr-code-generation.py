import qrcode
import os
import cv2 as cv
from qrcode.image.pure import PyPNGImage

#Double Checking Directory
print("Current working dir:", os.getcwd())

#QRCode creation class
qr=qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_H, box_size=50, border=1)

#Creates QRCode image using input and saves into images directory
block_name=input("Enter block name")
version=input("Enter QR code version")

qr.add_data(block_name)
img = qr.make_image(image_factory=qrcode.image.pure.PyPNGImage, fill_color="black", back_color="white")
imgsave=img.save(f'qr-code/images/version{version}/{block_name}.png')