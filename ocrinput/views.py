from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage  # for file acess
from PIL import Image
import pytesseract
import argparse
import cv2
import os


def image_to_text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text


# Create your views here.
def index(request):
    try:
        if request.method == 'POST' and request.FILES['file']:
            file = request.FILES['file']
            fs = FileSystemStorage()
            print(image_to_text(fs))
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            return render(request, 'ocrinput/page.html', {
                'uploaded_file_url': uploaded_file_url
            })
        return render(request, 'page.html')
    except:
        pass
