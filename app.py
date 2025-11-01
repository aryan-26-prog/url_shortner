import os
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, abort
)
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models import db, ShortURL, Click
from utils import generate_short_id, is_valid_url


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # ✅ Database Path (absolute)
    db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'instance', 'url_shortener.sqlite'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # ---------------- ROUTES ---------------- #

    # 🌐 Home Page
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html', title="Smart Shortener")

    # ✂️ Create Short URL (form)
    @app.route('/create', methods=['POST'])
    def create():
        data = request.form or request.json or {}
        original = data.get('url') or data.get('original_url')
        custom = data.get('custom_alias', None)

        if not original:
            flash('⚠️ Please provide a valid URL.', 'error')
            return redirect(url_for('index'))

        valid, fixed_url = is_valid_url(original)
        if not valid:
            flash('🚫 Invalid URL format. Please check and try again.', 'error')
            return redirect(url_for('index'))

        # 🔍 Check existing
        existing = ShortURL.query.filter_by(original_url=fixed_url).first()
        if existing and not custom:
            return render_template('created.html', short=existing, host=request.host_url)

        # 🔁 Generate & save short ID
        attempt = 0
        while attempt < 10:
            attempt += 1
            short_id = custom.strip() if custom else generate_short_id(6)
            try:
                new = ShortURL(
                    short_id=short_id,
                    original_url=fixed_url,
                    custom_alias=custom if custom else None
                )
                db.session.add(new)
                db.session.commit()
                flash('✅ Short URL created successfully!', 'success')
                return render_template('created.html', short=new, host=request.host_url)
            except IntegrityError:
                db.session.rollback()
                if custom:
                    flash('❌ Custom alias already taken. Try another one.', 'error')
                    return redirect(url_for('index'))
        flash('⚠️ Could not generate a unique short ID. Try again later.', 'error')
        return redirect(url_for('index'))

    # 🔗 API Route for JSON
    @app.route('/api/create', methods=['POST'])
    def api_create():
        payload = request.get_json() or {}
        original = payload.get('url')
        custom = payload.get('custom')

        if not original:
            return jsonify({'error': 'url missing'}), 400

        valid, fixed_url = is_valid_url(original)
        if not valid:
            return jsonify({'error': 'invalid url'}), 400

        existing = ShortURL.query.filter_by(original_url=fixed_url).first()
        if existing and not custom:
            return jsonify({
                'short_url': request.host_url + existing.display_id(),
                'id': existing.display_id()
            }), 200

        for _ in range(10):
            short_id = custom.strip() if custom else generate_short_id(6)
            try:
                new = ShortURL(
                    short_id=short_id,
                    original_url=fixed_url,
                    custom_alias=custom if custom else None
                )
                db.session.add(new)
                db.session.commit()
                return jsonify({
                    'short_url': request.host_url + new.display_id(),
                    'id': new.display_id()
                }), 201
            except IntegrityError:
                db.session.rollback()
                if custom:
                    return jsonify({'error': 'custom alias taken'}), 409
        return jsonify({'error': 'failed to generate short id'}), 500

    # 🚀 Redirect Short URL
    @app.route('/<string:short_id>')
    def redirect_short(short_id):
        short = ShortURL.query.filter(
            (ShortURL.custom_alias == short_id) | (ShortURL.short_id == short_id)
        ).first()

        if not short:
            return render_template('404.html', title="Not Found"), 404

        short.click_count = (short.click_count or 0) + 1
        click = Click(
            shorturl=short,
            ip=request.headers.get('X-Forwarded-For', request.remote_addr),
            user_agent=request.headers.get('User-Agent'),
            referrer=request.referrer
        )
        db.session.add(click)
        db.session.commit()
        return redirect(short.original_url)

    # 📊 Stats Page
    @app.route('/stats/<string:short_id>')
    def stats(short_id):
        short = ShortURL.query.filter(
            (ShortURL.custom_alias == short_id) | (ShortURL.short_id == short_id)
        ).first()
        if not short:
            abort(404)
        clicks = Click.query.filter_by(shorturl=short).order_by(
            Click.timestamp.desc()
        ).limit(100).all()
        return render_template('stats.html', short=short, clicks=clicks, title="URL Stats")

    # ❤️ Health Check
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok', 'time': datetime.utcnow().isoformat()})

    return app


# Run Flask app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
