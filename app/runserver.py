
#Define Python project in PYTHONPATH
import sys
from os.path import dirname, abspath
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.append(PROJECT_DIR)

#Initial project
from app import create_app
from werkzeug.contrib.fixers import ProxyFix

app = create_app(config_name='production')
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == "__main__":
    app.run(host='localhost', port=5444)