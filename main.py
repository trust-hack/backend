import sys, os

from internal.routes import app
from dotenv import load_dotenv
from tools import content

load_dotenv()

if __name__ == '__main__':
    SERVER_PORT = os.getenv("SERVER_PORT")
    SERVER_DEBUG = os.getenv("SERVER_DEBUG")

    if SERVER_PORT == None or SERVER_DEBUG == None:
        print(content.EnvVarsNotFound.format("SERVER_PORT or SERVER_DEBUG"))
        sys.exit(1)

    app.run(host="0.0.0.0", debug=SERVER_DEBUG, port=SERVER_PORT)
