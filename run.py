from api import create_app
from os import environ
from dotenv import load_dotenv

load_dotenv()
app = create_app()


@app.route('/status', methods=['GET'])
def status():
    return 'Running!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=environ.get('SERVER_CONTAINER_PORT',8080))