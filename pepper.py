#!/usr/bin/env python3
import asyncio
import json
import qi
import os
import websockets

#PEPPER_IP = "localhost"  # Cambia con l'IP di Pepper
PEPPER_IP = "10.100.10.162"
POLL_FILE = "poll.json"

PEPPER_PORT = 9559

scenes = {
    "Parthenope": [
        {"say": "Let me introduce you to the Università degli Studi di Napoli Parthenope, a historic university in Naples. It was founded in nineteen twenty as a Royal Naval Institute. Today, it offers a wide range of programs in computer science, economics, law, engineering, and sports sciences. Let me show you a brief overview of the university."},
        {"video": "images/parthenope.mp4"},
        {
            "question": "Do you know what the symbol of the Università degli Studi di Napoli Parthenope represents?",
            "options": ["A siren", "An anchor"],
            "answer": "A siren"
        },
        {"say": "The symbol of the university is a siren, which represents the mythical siren Parthenope, who is said to have founded the city of Naples."}
    ],

    "Brain Lab Team": [
        {"say": "The Brain Lab Team is a research group at the Università degli Studi di Napoli Parthenope. They focus on artificial intelligence, machine learning, and robotics."},
        {
            "question": "Do you know what our research focuses on?",
            "options": ["Human Computer Interface", "Robotics only"],
            "answer": "Human Computer Interface"
        },
        {"say": "Our team explores how the brain works, and how technology can support mental health, cognitive processes, and new ways of interacting with machines."}
    ],
    "Castel dell'Ovo": [
        {"say": "Il Castel dell'Ovo è il castello più antico di Napoli."},
        {
            "question": "Sai perché si chiama Castel dell'Ovo?",
            "options": ["Per la sua forma", "Per una leggenda di un uovo magico"],
            "answer": "Per una leggenda di un uovo magico"
        },
        {"say": "Secondo la leggenda, Virgilio nascose un uovo magico nelle fondamenta."}
    ],
    "ICSR 2025": [
        {"say": "Here are a few information about ICSR twenty twenty-five, the International Conference on Social Robotics. This year, it will take place in Naples from September tenth to twelfth. Researchers from all over the world will gather to discuss social robots, artificial intelligence, and their applications in healthcare, education, and society."},
        {
            "question": "What is the main theme of ICSR twenty twenty-five?",
            "options": ["Social Robotics", "Ancient Roman History"],
            "answer": "Social Robotics"
        },
        {"say": "Social robotics is about building robots that can interact naturally with humans, just like I’m doing right now."}
    ],
    "Social Events": [
        {"say": "Let me tell you about the social events at ICSR twenty twenty-five."},
        {"say": "First, the Welcome Reception will be held on September tenth at the Circolo Canottieri, a beautiful nautical club overlooking the bay of Naples."},
        {"say": "Then, on September eleventh there will be a Walking Tour of the historic center, a UNESCO World Heritage site."},
        {"say": "The Conference Dinner will take place on September eleventh at San Lorenzo Maggiore, a medieval complex with Roman ruins."},
        {"say": "Finally, the Closing Party is scheduled on September twelfth at Terrazza Flegrea, overlooking the sea—perfect to end the conference with style."},
    ],
    "Napoli": [
        {"say": "Naples is a city full of history, art, and traditions. It is known worldwide for pizza, music, and breathtaking views."},
        {
            "question": "Do you know which UNESCO site is in Naples?",
            "options": ["The Historic City Centre", "Mount Vesuvius"],
            "answer": "The Historic City Centre"
        },
        {"say": "The historic centre of Naples is one of the largest in Europe and a UNESCO World Heritage Site. It is home to numerous churches, palaces, and museums. On September eleventh, you will have the chance to visit it with a guided tour."}
    ],
    "Future of Robotics": [
        {"say": "Social robots like me are becoming part of daily life. They can help in education, healthcare, and even in supporting elderly people."},
        {
            "question": "Would you like robots to help more in healthcare or education?",
            "options": ["Healthcare", "Education"]
        },
        {"say": "Thank you for your opinion! Robots are not here to replace humans, but to support them and improve their quality of life."}
    ]



}

# Carica i contatori sondaggio all'avvio
def load_poll_data():
    if os.path.exists(POLL_FILE):
        with open(POLL_FILE, "r") as f:
            return json.load(f)
    else:
        return {"Future of Robotics": {"Healthcare": 0, "Education": 0}}

# Salva i contatori sul file
def save_poll_data(data):
    with open(POLL_FILE, "w") as f:
        json.dump(data, f)

class PepperServer:
    def __init__(self):
        self.session = qi.Session()
        try:
            self.session.connect(f"tcp://{PEPPER_IP}:{PEPPER_PORT}")
            print("[INFO] ✅ Connesso a Pepper!")
        except RuntimeError:
            print("[ERROR] ❌ Impossibile connettersi a Pepper.")
            exit(1)
        self.poll_data = load_poll_data()
        self.tts = self.session.service("ALTextToSpeech")
        self.animated_speech = self.session.service("ALAnimatedSpeech")
        self.motion = self.session.service("ALMotion")
        self.motion.wakeUp()
        self.tts.setLanguage("English")
        self.audio = self.session.service("ALAudioDevice")
        print("Volume globale attuale:", self.audio.getOutputVolume())
        self.audio.setOutputVolume(100)

        # Stato corrente
        self.current_card = None
        self.current_step_index = 0
        self.current_step_data = None
        self.expected_video = None

    async def speak(self, text):
        if not text:
            return
        try:
            self.animated_speech.say(text, {"bodyLanguageMode": "contextual"})
        except Exception as e:
            print("[WARN] AnimatedSpeech fallita, uso TTS:", e)
            self.tts.say(text)
        await asyncio.sleep(max(len(text) * 0.04, 1.0))

    async def send_question(self, websocket, step_data):
        await websocket.send(json.dumps({
            "question": step_data["question"],
            "options": step_data["options"]
        }))
        await self.speak(step_data["question"])

    async def send_result(self, websocket, selected, correct):
        await websocket.send(json.dumps({
            "selected": selected,
            "correct": correct
        }))
        if selected.lower() == correct.lower():
            await self.speak("Correct!")
        else:
            await self.speak(f"Too bad! The correct answer is {correct}.")

    async def process_next_step(self, websocket):
        """Processa uno step alla volta basandosi sull'indice corrente."""
        if not self.current_card:
            return

        steps = scenes[self.current_card]
        if self.current_step_index >= len(steps):
            # Fine card
            await websocket.send(json.dumps({"hide_btn": "block"}))
            self.current_card = None
            self.current_step_index = 0
            self.current_step_data = None
            self.expected_video = None
            return

        step = steps[self.current_step_index]

        # Discorso
        if "say" in step:
            await self.speak(step["say"])
            self.current_step_index += 1
            await self.process_next_step(websocket)

        # Video
        elif "video" in step:
            self.expected_video = step["video"]
            await websocket.send(json.dumps({"show_video": step["video"]}))
            # Aspetta evento video_ended
            # Non incrementiamo qui, lo faremo quando riceviamo il messaggio
            print(f"[INFO] Attendo la fine del video {step['video']}")

        # Domanda
        elif "question" in step:
            self.current_step_data = step
            await self.send_question(websocket, step)
            # Aspetta risposta, non incrementiamo ancora
        elif "photo" in step:
            await websocket.send(json.dumps({"show_photo": step["photo"]}))
            self.current_step_index += 1
            await self.process_next_step(websocket)

    async def handler(self, websocket):
        async for message in websocket:
            data = json.loads(message)
            print(f"[DEBUG] Messaggio ricevuto: {data}")

            # Selezione card
            if "card" in data:
                self.current_card = data["card"]
                self.current_step_index = 0
                await websocket.send(json.dumps({"hide_btn": "none"}))
                await self.process_next_step(websocket)

            # Risposta domanda
            elif "answer" in data and self.current_step_data:
                selected = data["answer"]
                if self.current_card == "Future of Robotics":
                    if selected in self.poll_data["Future of Robotics"]:
                        self.poll_data["Future of Robotics"][selected] += 1
                        save_poll_data(self.poll_data)
                        print(f"[INFO] Poll aggiornata: {self.poll_data}")
                        await websocket.send(json.dumps({"update_poll": self.poll_data["Future of Robotics"]}))
                if "answer" in self.current_step_data:
                    correct = self.current_step_data["answer"]
                    await self.send_result(websocket, selected, correct)

                await websocket.send(json.dumps({"hide_question": True}))
                self.current_step_index += 1
                await self.process_next_step(websocket)

            # Fine video
            elif "video_ended" in data:
                if data["video_ended"] == self.expected_video:
                    self.current_step_index += 1
                    self.expected_video = None
                    await self.process_next_step(websocket)

    async def start_server(self):
        async with websockets.serve(self.handler, "0.0.0.0", 8765):
            print("[INFO] WebSocket server started on ws://0.0.0.0:8765")
            await asyncio.Future()

if __name__ == "__main__":
    server = PepperServer()
    asyncio.run(server.start_server())
