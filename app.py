from flask import Flask, render_template, url_for
import os
from models import db, Mahasiswa
from uploads import uploads_bp

def create_app(db_path='sqlite:///mahasiswa.db'):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('FLASK_SECRET', 'ubah-ke-secret-anda')

    db.init_app(app)

    # ensure static subfolders exist
    os.makedirs(os.path.join(app.static_folder, 'backgrounds'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'photos'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'js'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'css'), exist_ok=True)

    app.register_blueprint(uploads_bp)

    @app.route('/')
    def index():
        # choose background url if exists
        bg_path = os.path.join(app.static_folder, 'backgrounds', 'current_bg.jpg')
        if not os.path.exists(bg_path):
            # try other extensions if needed
            alternatives = ['current_bg.png', 'current_bg.jpeg', 'current_bg.gif']
            for alt in alternatives:
                if os.path.exists(os.path.join(app.static_folder, 'backgrounds', alt)):
                    bg_path = os.path.join(app.static_folder, 'backgrounds', alt)
                    break
            else:
                bg_path = None
        bg_url = url_for('static', filename='backgrounds/' + os.path.basename(bg_path)) if bg_path else None
        mhs = Mahasiswa.query.order_by(Mahasiswa.nim).limit(200).all()
        return render_template('index.html', mhs=mhs, bg_url=bg_url)

    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
