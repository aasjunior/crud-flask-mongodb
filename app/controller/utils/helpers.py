from PIL import Image
from uuid import uuid4
from bson.binary import Binary
import os
import glob

def clear_tmp():
    # Remover todos os arquivos na pasta 'views/static/tmp/imgs'
    files = glob.glob('views/static/tmp/imgs/*')
    for f in files:
        os.remove(f)

class ImageProcessor:
    @staticmethod
    def save_as_png(image):
        # Gera um UUID e adiciona a extensão do arquivo
        filename = ImageProcessor.generate_unique_filename('png')
        dir_path = os.path.join('views', 'static', 'tmp', 'imgs')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        temp_image_path = os.path.join(dir_path, filename)
        image.save(temp_image_path)

        img = Image.open(temp_image_path)
        png_image_path = temp_image_path.rsplit('.', 1)[0] + '.png'
        img.save(png_image_path, 'PNG')

        return png_image_path
    
    @staticmethod
    def generate_unique_filename(extension):
        # gerar um UUID usando o algoritmo MD5
        unique_id = uuid4()
        # converter o UUID em uma string hexadecimal
        unique_name = unique_id.hex
        # adicionar a extensão do arquivo de imagem ao nome único
        filename = unique_name + '.' + extension
        return filename
    
    @staticmethod
    def encoded_image_binary(image):
        png_image_path = ImageProcessor.save_as_png(image)
        with open(png_image_path, 'rb') as f:
            encoded_image = Binary(f.read())
        
        return encoded_image
    
    @staticmethod
    def encoded_image_binary(image_path):
        with open(image_path, 'rb') as f:
            encoded_image = Binary(f.read())
        
        return encoded_image