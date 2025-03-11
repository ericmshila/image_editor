from PIL import Image, ImageEnhance


def darken():
    img = Image.open('./images/car.jpg')
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.25)
    img.save('./darkcar.png')

def resize():
    img = Image.open('./images/car.jpg')

darken()
    