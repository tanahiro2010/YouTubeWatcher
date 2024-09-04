from config import ConfigParser
from flask import Flask, send_file, request, render_template
from flask_httpauth import HTTPBasicAuth
from app import YouTube
from uuid import uuid4
import asyncio

# YouTube閲覧に入るためのセキュリティ
allow_id = []
allow_investigate_id = {}
watch_video_id = {}

# サーバー関連設定
config = ConfigParser()
config.load_config(file_path='server.conf')
host = config.get('host')
port = 80
try:
    port = int(config.get('port'))
except ValueError:
    print('{}PORT in the server configuration file is Set it as an integer.\nUsing PORT 80 due to error.{}'.format('\033[31m', '\033[0m'))
root = config.get('root_directory')
password = config.get('password')

# サーバー関連
app = Flask(__name__, template_folder=root)
auth = HTTPBasicAuth()
user_data = {
    'admin': 'Kirigayakazuto1',
    'tanahiro2010': 'Kirigayakazuto1'
}

YouTube = YouTube(api_token='AIzaSyCeTZtv9BC4FLVrmiJjd8L_GfuYM3V2UuQ')

@auth.get_password
def get_password(username):
    if username in user_data:
        return user_data[username]

@app.route('/api/youtube/video/<video_id>', methods = ["GET"])
def youtube_video_download(video_id):
    file_name = YouTube.download_youtube_video(video_id=video_id)['default']
    return send_file(file_name, mimetype='video/mp4')

@app.route('/api/youtube/investigate/<query>', methods = ["GET"])
def youtube_investigate(query):
    investigate_id: str = str(uuid4())
    videos_data = YouTube.investigate_video(query=query)
    allow_investigate_id[investigate_id] = videos_data
    return "/investigate/" + investigate_id


@app.route('/api/investigate/<query>', methods = ["GET"])
def investigate(query):
    return YouTube.investigate_video(query=query)

@app.route('/api/comment/value/<value>', methods = ["GET"])
def api_comment_value(value):
    id: str = str(uuid4())
    if value == password:
        allow_id.append(id)

    return 'true:/comment/{}'.format(id)

@app.route('/api/watch_comment/<video_id>', methods = ["GET"])
def api_watch_comment(video_id):
    session_id = str(uuid4())
    watch_video_id[session_id] = video_id

    return "/watch_comment/{}".format(session_id)






# Web関連
@app.route('/')
def index():
    return render_template('index.html'.format(root))

@app.route('/comment/<id>', methods = ["GET"])
def comment(id):
    print("Request comment.\nID: {}\nIP_Address: {}".format(id, request.remote_addr))
    if id in allow_id:
        print('Request Allowed.')
        return render_template("youtube-home.html".format(root), video_objects=YouTube.investigate_video('tanahiro2010'))
    else:
        print('Request DisAllowed.')
        return render_template('disallow.html'.format(root))

@app.route('/investigate/<investigate_id>', methods = ["GET"])
def video_investigate(investigate_id):
    print('Investigate request\nID: {}\nIP_Address: {}'.format(investigate_id, request.remote_addr))
    if investigate_id in allow_investigate_id:
        print('Request Allowed.')
        return render_template("investigate.html".format(root), video_objects=allow_investigate_id[investigate_id])
    else:
        print('Request DisAllowed.')
        return render_template('disallow.html'.format(root))

@app.route('/watch_comment/<session_id>', methods = ["GET"])
def watch_video(session_id):
    if session_id in watch_video_id.keys():
        video_id = watch_video_id[session_id]
        video_data = YouTube.fetch_video(video_id=video_id)

        print(video_data)

        title = video_data['snippet']['title']
        description = video_data['snippet']['description'].format('\n', '<br>')

        return render_template('watch.html'.format(root), video_url='/api/youtube/video/{}'.format(watch_video_id[session_id]), title=title, description=description)
    else:
        return render_template('index.html'.format(root))

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)