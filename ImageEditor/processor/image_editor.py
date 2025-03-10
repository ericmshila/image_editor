from flask import Flask, request, send_file, render_template
import cv2
import numpy as np 
import io
from PIL import Image, ImageEnhance, ImageFilter


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')


def get_file():
     # ensure file upload
    if 'file' not in request.files:
        return {'error: No file uploaded'}, 400
    file = request.files['file'] #retrieve file
    image_bytes = file.read() # read contents 
    return image_bytes

def convert_greyscale(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert('L')
    return image

#IMAGE PROCESSOR
def deblur_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)) #opens the image as a BINARY STREAM as if it weas beinG read from a file
    image = image.filter(ImageFilter.SHARPEN)
    image = np.array(image) #convert to numerical values that can be manipulated

    #kernel as a nested list that defines array elements as a matrix
    # 5 - current pixel. -1 surrounding elements
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)

    deblurred = cv2.filter2D(image, -1, kernel) #applies kernel to image pixel by pixel. -1 =is desired depth of output
    return Image.fromarray(deblurred) #reverse of np.array(image). Creates PIL image from numpy array

@app.route("/grayscale", methods = ["POST"])
def greyscale():
   
    greyscale_image = convert_greyscale( get_file())
    img_io = io.BytesIO()
    greyscale_image.save(img_io, format = "PNG")
    img_io.seek(0) #resets pointer so you can read the data from the start
    return send_file(img_io, mimetype='image/png')


@app.route("/deblur", methods=["POST"])
#API HANDLER
def deblur():
    
    deblurred_image = deblur_image(get_file()) # call deblur image function
    img_io = io.BytesIO() #shorten the io.BytesIO class. Allows you to use im_memory_file as a file object
    deblurred_image.save(img_io, format="PNG") # save image in PNG format
    img_io.seek(0) #resets pointer so you can read the data from the start
    return send_file(img_io, mimetype='image/png') #sends response to client



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)


