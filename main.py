import yt_dlp
import sys
import os
from flask import Flask, request, render_template_string, send_file, jsonify, send_from_directory
from win10toast import ToastNotifier

def download_audio(url, output_path=os.path.join(os.path.expanduser('~'), 'Downloads')):
    """
    Download audio from YouTube URL.
    Supports single videos and playlists.
    """
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': False,  # Allow playlist downloads
    }

    try:
        os.makedirs(output_path, exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed successfully!")
        os.startfile(output_path)  # Open the folder
        toaster = ToastNotifier()
        toaster.show_toast("Download Complete", "Your music has been downloaded successfully!", duration=5)
    except Exception as e:
        print(f"Error downloading: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/styles.css')
def styles():
    return send_file('styles.css')

@app.route('/script.js')
def script():
    return send_file('script.js')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    try:
        download_audio(url)
        return jsonify({'message': 'Download completed successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/downloads/<path:filename>')
def download_file(filename):
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    return send_from_directory(downloads_path, filename, as_attachment=True)

def main():
    if len(sys.argv) < 2:
        print("https://youtu.be/P1gnCQhoEYQ?si=ZBDhC7dX-F9X6rVL")
        sys.exit(1)

    url = sys.argv[1]
    download_audio(url)

if __name__ == "__main__":
    app.run(debug=True)