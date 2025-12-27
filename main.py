import asyncio
import threading
import time
import base64
import pyautogui
import pyaudiowpatch as pyaudio
from flask import Flask, render_template, jsonify
from flask_sock import Sock
from winsdk.windows.storage.streams import DataReader, Buffer, InputStreamOptions

# Попытка импорта SDK
try:
    from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager, GlobalSystemMediaTransportControlsSessionPlaybackStatus
except ImportError:
    GlobalSystemMediaTransportControlsSessionManager = None

SAMPLE_RATE = 48000
CHUNK_SIZE = 2048
CHANNELS = 2

app = Flask(__name__)
sock = Sock(app)

# Хранилище состояния
current_track_info = {
    "title": "Ожидание...", 
    "artist": "", 
    "thumbnail": "", 
    "cached_title_check": "",
    "timeline": {"position": 0, "duration": 0, "playback_status": "Stopped"}
}
last_known_title = ""

# --- ЧТЕНИЕ ОБЛОЖКИ ---
async def read_stream_into_buffer(stream_ref, buffer_size=5000000):
    try:
        readable_stream = await stream_ref.open_read_async()
        win_buffer = Buffer(buffer_size) 
        await readable_stream.read_async(win_buffer, buffer_size, InputStreamOptions.READ_AHEAD)
        if win_buffer.length == 0: return None
        data_reader = DataReader.from_buffer(win_buffer)
        bytes_data = bytearray(win_buffer.length)
        data_reader.read_bytes(bytes_data)
        return bytes(bytes_data)
    except: return None

# --- СБОР ИНФОРМАЦИИ ---
async def get_media_info():
    global last_known_title
    if not GlobalSystemMediaTransportControlsSessionManager: return None
    
    try:
        sessions = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        current_session = sessions.get_current_session()
        
        if current_session:
            # 1. Свойства медиа (Название, Автор, Обложка)
            props = await current_session.try_get_media_properties_async()
            
            # 2. Свойства времени (Timeline)
            timeline = current_session.get_timeline_properties()
            playback_info = current_session.get_playback_info()
            
            # Конвертация статуса в строку
            status_enum = playback_info.playback_status
            status_str = "Playing"
            if status_enum == GlobalSystemMediaTransportControlsSessionPlaybackStatus.PAUSED: status_str = "Paused"
            elif status_enum == GlobalSystemMediaTransportControlsSessionPlaybackStatus.STOPPED: status_str = "Stopped"

            result = {
                "title": props.title,
                "artist": props.artist,
                "thumbnail": None,
                "timeline": {
                    "position": timeline.position.total_seconds() if timeline.position else 0,
                    "duration": timeline.end_time.total_seconds() if timeline.end_time else 0,
                    "playback_status": status_str
                }
            }

            # Грузим картинку только если сменился трек
            if props.title != last_known_title:
                last_known_title = props.title
                if props.thumbnail:
                    img_bytes = await read_stream_into_buffer(props.thumbnail)
                    if img_bytes:
                        result["thumbnail"] = base64.b64encode(img_bytes).decode('utf-8')
            
            return result
    except: pass
    return None

def media_info_looper():
    if GlobalSystemMediaTransportControlsSessionManager is None: return
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        try:
            info = loop.run_until_complete(get_media_info())
            if info:
                current_track_info["title"] = info["title"]
                current_track_info["artist"] = info["artist"]
                current_track_info["timeline"] = info["timeline"]
                
                if info["thumbnail"] is not None:
                    current_track_info["thumbnail"] = info["thumbnail"]
                elif info["title"] != current_track_info.get("cached_title_check"):
                    current_track_info["thumbnail"] = ""
                
                current_track_info["cached_title_check"] = info["title"]
        except: pass
        time.sleep(1.0)

threading.Thread(target=media_info_looper, daemon=True).start()

# --- AUDIO ---
@sock.route('/audio_ws')
def audio_socket(ws):
    p = pyaudio.PyAudio()
    stream = None
    try:
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
            else: default_speakers = p.get_default_wasapi_loopback()

        stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=SAMPLE_RATE,
                        input=True, input_device_index=default_speakers["index"], frames_per_buffer=CHUNK_SIZE)

        while True:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            ws.send(data)
    except: pass
    finally:
        if stream: stream.stop_stream(); stream.close()
        p.terminate()

# --- ROUTES ---
@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/status')
def status(): return jsonify(current_track_info)

@app.route('/api/next', methods=['POST'])
def next_track():
    pyautogui.press('nexttrack')
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print(f"🚀 Started: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, threaded=True)
