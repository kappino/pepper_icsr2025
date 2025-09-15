# Pepper Infotainment

Questo progetto implementa un sistema di **interazione multimodale con il robot Pepper**, combinando:
- **Backend in Python** → gestisce la connessione con Pepper e un server WebSocket.
- **Frontend Web (HTML/JS/CSS)** → interfaccia grafica per visualizzare contenuti multimediali e domande a risposta multipla.

Lo scopo è fornire una piattaforma semplice e interattiva per presentazioni con il supporto di Pepper.

---

## 📦 Requirements

### Python
- Python 3.8+  
- Pacchetti Python:
- [qi](https://github.com/aldebaran/libqi-python)
```bash
  pip install websockets asyncio qi
````

### Frontend

* Qualsiasi browser moderno (Chrome, Firefox, Edge).
* Accesso in rete al server Python via WebSocket (porta `8765` di default).

---

## 🚀 Installazione e avvio

1. Clonare o copiare la repository sul proprio computer.
2. Verificare l’IP di Pepper (aggiornare la variabile `PEPPER_IP` in `server.py`).
3. Avviare il server:

   ```bash
   python3 server.py
   ```
4. Aprire `index.html` nel browser (sul PC o su un dispositivo connesso alla stessa rete).
5. Cliccare sulle cards per avviare le scene e interagire con Pepper.

---

## 📂 Struttura del progetto

```
.
├── server.py       # Backend Python, gestisce Pepper + WebSocket server
├── poll.json       # File di salvataggio per i sondaggi
├── index.html      # Frontend Web (HTML, CSS, JS)
├── images/         # Risorse grafiche (icone, GIF, foto, ecc.)
└── videos/         # Video utilizzati nelle scene
```

---

## ⚙️ Funzionalità attuali

* Gestione di **scene** predefinite (Parthenope, Brain Lab Team, Napoli, ICSR, ecc.).
* Supporto per:

  * Testo parlato (TTS + AnimatedSpeech di Pepper).
  * Video e immagini.
  * Domande a risposta multipla con feedback immediato.
* Sondaggio persistente per la scena *Future of Robotics* (`poll.json`).
* Interfaccia grafica web con griglia di card interattive.

---

## 🔮 Possibili upgrade futuri

* **Protocollo WebSocket più strutturato**
  Inviare messaggi con un campo `type` (`scene`, `question`, `video`, ecc.) per rendere il client più modulare e semplice da estendere.

* **Separazione contenuti/logica**
  Spostare le scene in un file JSON esterno, così da poter aggiungere/modificare contenuti senza toccare il codice Python.

* **Logging migliorato**
  Sostituire i `print` con il modulo `logging` di Python per avere log più leggibili e configurabili.

* **Interfaccia responsive e modulare**
  Migliorare l’UI con un framework leggero (Vue.js, Svelte) per rendere il frontend più dinamico.

* **App mobile / PWA**
  Convertire l’interfaccia in una **Progressive Web App** o pacchettizzarla come app Android/iOS tramite **Capacitor** o **Cordova**.

* **Multi-utente / Multi-device**
  Estendere il server per gestire più connessioni WebSocket contemporaneamente (es. più tablet collegati a Pepper).

---

## 👨‍💻 Autore

Progetto sviluppato da **Crescenzo Esposito** – Università degli Studi di Napoli *Parthenope*.
Versione: 1.0 (Settembre 2025).

```

