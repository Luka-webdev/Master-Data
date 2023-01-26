from main import app
from views.welcome_screen import make_layout

if __name__ == '__main__':
    app.layout = make_layout()
    app.run_server()
