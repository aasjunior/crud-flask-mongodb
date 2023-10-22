from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PIL import Image
import os

class DBConfig:
    """
    A classe DBConfig é responsável por carregar as variáveis de ambiente do arquivo .env e fornecer
    os detalhes do banco de dados quando necessário. Isso é feito para evitar a duplicação de código
    e manter a configuração do banco de dados em um único lugar.

    Métodos
    -------
    get_db_details():
        Retorna os detalhes do banco de dados como host, port, db_name, username e password.
    """
    load_dotenv()

    @staticmethod
    def get_db_config():
        host = os.getenv('MONGODB_HOST')
        port = int(os.getenv('MONGODB_PORT'))
        db_name = os.getenv('MONGODB_DATABASE')
        username = os.getenv('MONGODB_USERNAME')
        password = os.getenv('MONGODB_PASSWORD')

        return host, port, db_name, username, password
    
class ImageProcessor:
    @staticmethod
    def save_as_png(image):
        filename = secure_filename(image.filename)
        temp_image_path = os.path.join('views', 'static', 'tmp', 'imgs', filename)
        image.save(temp_image_path)

        img = Image.open(temp_image_path)
        png_image_path = temp_image_path.rsplit('.', 1)[0] + '.png'
        img.save(png_image_path, 'PNG')

        return png_image_path
