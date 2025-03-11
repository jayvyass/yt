from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "static/downloads"  # Save files in 'static/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(link):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("\n📥 Downloading...")
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)
            print("✅ Download completed!\n")
            return filename
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_link = request.form['video_link'].strip()
        file_path = download_video(video_link)
        if file_path:
            filename = os.path.basename(file_path)
            return render_template('index.html', filename=filename)
    return render_template('index.html', filename=None)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
