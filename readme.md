# 🎵 PC Audio Streamer

**Turn your phone into a wireless speaker for your PC.**

A low-latency audio streaming server written in Python. It captures your Windows PC audio (WASAPI Loopback) and streams it to any device via a web browser. No app installation required on the client side — just open the link.

Perfect for watching movies from your couch, listening to music while cleaning the room, or turning an old phone into a dedicated PC speaker.

![Interface Screenshot](https://s4.iimage.su/s/27/gNgbJOwxOiTwuLWCDlwzEXts3RazL9FNCnRRz2d6.png)

## ✨ Key Features

- **Zero App Install**: Works seamlessly in Chrome/Safari on Android & iOS.
- **Low Latency**: Uses WebSockets + RAW PCM stream. Delay is minimal (<0.1s on 5GHz Wi-Fi), suitable for videos.
- **High Quality**: Streams uncompressed 48kHz Stereo Audio.
- **Rich Metadata**: Automatically fetches current Track, Artist, Album Art, and Progress Bar from Windows (works with Spotify, Chrome, YouTube, System sounds).
- **Remote Control**: Play, Pause, and Skip tracks directly from your phone.
- **Adaptive UI**: Modern "Glassmorphism" design with animated album art and adaptive background colors.

## 🛠 Tech Stack

- **Backend**: Python, Flask, Flask-Sock
- **Audio Capture**: PyAudioWPatch (WASAPI Loopback support)
- **System Integration**: WinSDK (Windows Runtime API for Media Controls)
- **Frontend**: HTML5, Vanilla JS, Web Audio API, WebSockets

## 🚀 Installation

### Prerequisites
- Windows 10 or 11 (Required for Loopback & Media API)
- Python 3.7 or higher

### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/pc-audio-streamer.git
cd pc-audio-streamer
```

2. **Create a virtual environment (Recommended):**
`python -m venv venv`

Activate on Windows:
`venv\Scripts\activate`

3. **Install dependencies:**
`pip install -r requirements.txt`

## 🎮 Usage

1. **Start the server:**
`python main.py`

2. **Connect from your phone:**
- The script will print your local IP address, e.g., `http://192.168.1.5:5000`.
- Ensure your phone and PC are connected to the **same Wi-Fi network**.
- Open the link in your phone's browser (Chrome or Safari recommended).

3. **Tap "Start Stream"** on the phone screen. Audio should start playing immediately.

## ⚙️ Configuration

You can tweak settings in `main.py` if needed:

```py
SAMPLE_RATE = 48000 # Audio quality (44100 or 48000)
CHUNK_SIZE = 2048 # Lower = lower latency but higher CPU/Network load
```

## ❓ Troubleshooting

**Audio is stuttering / clicking?**
- Ensure you are on a **5GHz Wi-Fi** network. 2.4GHz might be too slow for uncompressed audio.
- Increase `CHUNK_SIZE` in `main.py` to `4096` for better stability (at cost of slight latency).

**Album Art is pixelated?**
- This is a limitation of Windows Media API (SMTC), which provides low-res thumbnails for system integration. The web interface applies CSS smoothing and blur effects to mitigate this.

**"No loopback device found" error?**
- Ensure your speakers/headphones are set as the **Default Device** in Windows Sound Settings and are currently active.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---
*Created with ❤️ by EggZys*