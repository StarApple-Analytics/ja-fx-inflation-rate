from werkzeug.middleware.proxy_fix import ProxyFix
from api import create_app

app = create_app()

# Fix to nginx reverse proxy issues (if any, uncomment commented lines)
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
	app.run()