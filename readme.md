<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,14&height=180&section=header&text=🎵%20SoundBeam&fontSize=60&fontColor=fff&fontAlignY=55&desc=Turn+your+phone+into+a+wireless+PC+speaker&descSize=16&descAlignY=75&animation=twinkling" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![WebSockets](https://img.shields.io/badge/WebSockets-010101?style=for-the-badge&logo=socketdotio&logoColor=white)
![Windows](https://img.shields.io/badge/Windows%2010%2F11-0078D4?style=for-the-badge&logo=windows&logoColor=white)

<br/>

> **Захвати системный звук Windows и стримь его на телефон через браузер.**
> Никаких приложений. Только открыть ссылку — и слушать.

<br/>

<img src="https://raw.githubusercontent.com/EggZys/SoundBeam/main/assets/screenshot.png" width="300"/>

</div>

---

## ✨ Возможности

| | |
|---|---|
| 📱 **Zero Install** | Работает в Chrome / Safari на Android и iOS — без APK, без App Store |
| ⚡ **Low Latency** | WebSocket + RAW PCM поток. Задержка < 0.1s на 5GHz Wi-Fi — пригодно для видео |
| 🎧 **High Quality** | Несжатый звук 48kHz Stereo |
| 🎨 **Rich UI** | Glassmorphism-интерфейс с анимированной обложкой и адаптивным фоном |
| 🎵 **Метаданные** | Трек, исполнитель, обложка, прогресс-бар — из Windows SMTC (Spotify, YouTube, Chrome) |
| ⏯ **Remote Control** | Play / Pause / Skip прямо с телефона |

---

## 🔧 Как это работает

```
┌─────────────────────┐      WebSocket       ┌──────────────────────┐
│       Windows PC    │  ──────────────────→  │    Phone / Browser   │
│                     │                       │                       │
│  WASAPI Loopback    │   RAW PCM 48kHz       │    Web Audio API      │
│  (системный звук)   │  ──────────────────→  │    (воспроизведение)  │
│                     │                       │                       │
│  WinSDK / SMTC  ────┼── метаданные трека ─→ │    UI + обложка       │
└─────────────────────┘                       └──────────────────────┘
```

---

## 🚀 Установка

### Требования

- Windows 10 / 11
- Python 3.7+
- Телефон и PC в **одной Wi-Fi сети**

### Шаги

```bash
# 1. Клонировать репозиторий
git clone https://github.com/EggZys/SoundBeam.git
cd SoundBeam

# 2. Виртуальное окружение (рекомендуется)
python -m venv venv
venv\Scripts\activate

# 3. Зависимости
pip install -r requirements.txt
```

---

## 🎮 Запуск

```bash
python main.py
```

Скрипт выведет локальный IP, например `http://192.168.1.5:5000`.
Открой эту ссылку в браузере телефона → нажми **Start Stream**.

---

## ⚙️ Настройки

В `main.py` можно изменить:

```python
SAMPLE_RATE = 48000  # 44100 или 48000
CHUNK_SIZE  = 2048   # меньше = меньше задержка, выше нагрузка на сеть
```

---

## ❓ Troubleshooting

<details>
<summary><b>Треск / заикания в звуке</b></summary>
<br/>

- Используй **5GHz Wi-Fi** — 2.4GHz может не справляться с несжатым потоком
- Увеличь `CHUNK_SIZE` до `4096` для стабильности (незначительно растёт задержка)

</details>

<details>
<summary><b>Пикселизированная обложка</b></summary>
<br/>

Ограничение Windows Media API (SMTC) — он возвращает низкое разрешение.
Интерфейс применяет CSS blur и smoothing для компенсации.

</details>

<details>
<summary><b>"No loopback device found"</b></summary>
<br/>

Убедись, что колонки / наушники установлены как **Default Device** в настройках звука Windows и активны.

</details>

---

## 🛠 Стек

| Слой | Технология |
|------|-----------|
| Backend | Python · Flask · Flask-Sock |
| Захват звука | PyAudioWPatch (WASAPI Loopback) |
| Метаданные | WinSDK (Windows Runtime API / SMTC) |
| Frontend | HTML5 · Vanilla JS · Web Audio API · WebSockets |

---

## 📄 Лицензия

MIT — используй свободно.

---

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,14&height=100&section=footer" width="100%"/>

<div align="center">
<sub>Made with 🎵 by <a href="https://github.com/EggZys">EggZys</a></sub>
</div>
