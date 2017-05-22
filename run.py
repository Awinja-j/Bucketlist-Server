import os
from app import create_app
from flask import render_template



config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)


@app.route('/')
def landing_page():
    return render_template('landing_page.html')





if __name__ == '__main__':
    app.debug = True
    app.run()

