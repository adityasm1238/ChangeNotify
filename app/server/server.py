from flask import Flask
import dotenv
import os

dotenv.load_dotenv()

staticFolder = os.environ['STATIC_DIRECTORY']
print(staticFolder)
app = Flask(__name__,
            static_url_path='', 
            static_folder=staticFolder)