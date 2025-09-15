# Pepper Infotainment

Questo progetto implementa un sistema di **interazione con il robot Pepper**, combinando:

* **Backend in Python** → gestisce la connessione con Pepper e un server WebSocket.
* **Frontend Web (HTML/JS/CSS)** → interfaccia grafica per visualizzare contenuti multimediali e domande a risposta multipla.

L’obiettivo è fornire una piattaforma **semplice, estensibile e interattiva** per presentazioni e dimostrazioni supportate da Pepper.

---

## 📦 Requirements

### Python

* **Python 3.8+**
* Pacchetti necessari:

```bash
pip install websockets qi aiohttp aiofiles
```

* Libreria `qi` ([libqi-python](https://github.com/aldebaran/libqi-python)) → necessaria per comunicare con Pepper.

### Frontend

* Browser moderno (Chrome, Firefox, Edge).
* Accesso in rete al server Python via WebSocket (porta `8765` di default).

---

## 🚀 Installazione e avvio

1. Clonare o copiare la repository sul proprio computer.
2. Impostare l’IP di Pepper in `pepper.py`:

```python
PEPPER_IP = "192.168.1.xxx"
```

3. Avviare il **server Pepper + WebSocket**:

```bash
python3 pepper.py
```

4. Avviare il **server web** per servire `index.html` e i media:

```bash
python3 server.py
```

5. Aprire `index.html` in un browser:

* sullo stesso PC, oppure
* da un altro dispositivo nella stessa rete.

6. Interagire con Pepper cliccando sulle **card** disponibili.

---

## 📂 Struttura del progetto

```
.
├── pepper.py       # Gestione Pepper + server WebSocket
├── server.py       # Server web per frontend (HTML, immagini, video)
├── poll.json       # File per salvare i risultati dei sondaggi
├── index.html      # Frontend Web (HTML, CSS, JS)
├── images/         # Risorse grafiche (icone, GIF, foto, video)
└── videos/         # Video utilizzati nelle scene (opzionale)
```

---

## ⚙️ Funzionalità attuali

* Gestione di **scene predefinite**:
  Parthenope, Brain Lab Team, Napoli, ICSR, Social Events, Future of Robotics.
* Supporto per:

  * Parlato (TTS + AnimatedSpeech di Pepper)
  * Immagini e video
  * Domande a risposta multipla con feedback immediato
* **Sondaggio persistente** per *Future of Robotics*, salvato in `poll.json`.
* Interfaccia grafica web con griglia di card interattive.
* Streaming video con supporto agli header HTTP Range (necessario per `<video>`).

---

## 🔮 Possibili upgrade futuri

* **Protocollo WebSocket più strutturato**: aggiungere un campo `type` (`scene`, `question`, `video`) nei messaggi.
* **Separazione contenuti/logica**: spostare le scene in un file JSON esterno per facilitare aggiornamenti.
* **UI migliorata**: rendere l’interfaccia responsive e modulare, con framework leggero.
* **App mobile / PWA**: trasformare il frontend in una Progressive Web App o pacchettizzarlo come apk.
* **Multi-utente / multi-device**: gestire più tablet/browser collegati contemporaneamente.

---

## 👨‍💻 Autore

Progetto sviluppato da **Crescenzo Esposito** – Università degli Studi di Napoli *Parthenope*.
**Versione:** 1.0 (Settembre 2025)
