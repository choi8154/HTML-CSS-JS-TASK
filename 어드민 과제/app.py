from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dain8154@localhost/WorkOutDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dain8154'

db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), nullable=False)
    login_id = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    sex = db.Column(db.Enum('male', 'female'))
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Numeric(10, 2))
    weight = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.user_name}>'
    
    def get_id(self):
        return str(self.user_id)

class Playlist(db.Model):
    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    singer = db.Column(db.String(200), nullable=False)
    youtube_link = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # 🎵 카테고리 추가
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'))
    user = db.relationship("Users", backref=db.backref("playlist", lazy=True))


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# 홈페이지 라우터(로그인 전 보일 페이지)
@app.route('/')
def index():
    return 'Home Page'

# 플레이리스트 라우트
@app.route('/playlist')
@login_required
def playlist():
    search = request.args.get("search", "")  # 검색어
    page = request.args.get("page", 1, type=int)  # 페이지 번호
    per_page = 5  # 페이지당 곡 개수

    query = Playlist.query.filter_by(user_id=current_user.user_id)

    # 검색어 있으면 제목/가수명에서 검색
    if search:
        query = query.filter(
            (Playlist.title.contains(search)) | (Playlist.singer.contains(search))
        )

    # 페이지네이션
    songs = query.order_by(Playlist.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template("admin.html", user=current_user, songs=songs, search=search)


# 회원가입 라우트
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        login_id = request.form['login_id']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
        phone = request.form['phone']
        sex = request.form['sex']
        height = request.form['height']
        weight = request.form['weight']
        # 유저 생성
        new_user = Users(
            user_name=user_name,
            login_id=login_id,
            email=email,
            phone=phone,
            sex=sex,
            height=height,
            weight=weight
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

# 로그인 라우터(로그인 할 때 보이는 페이지)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id= request.form['login_id']
        password = request.form['password']
        user = Users.query.filter_by(login_id=login_id).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('playlist'))
        
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#곡추가 라우트
@app.route('/add_song', methods=['POST'])
@login_required
def add_song():
    title = request.form['title']
    singer = request.form['singer']
    youtube_link = request.form['youtube']
    category = request.form['category']

    new_song = Playlist(
        title=title,
        singer=singer,
        youtube_link=youtube_link,
        category=category,
        user_id=current_user.user_id
    )
    db.session.add(new_song)
    db.session.commit()

    return redirect(url_for('playlist'))

if __name__ == "__main__":
    app.run(debug=True)