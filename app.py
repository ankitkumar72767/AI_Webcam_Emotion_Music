from flask import Flask, request, jsonify, render_template, Response
import cv2
from deepface import DeepFace

app = Flask(__name__)

# Initialize webcam
camera = cv2.VideoCapture(0)  # Try 1 or 2 if black screen continues

if not camera.isOpened():
    print("❌ Error: Could not open webcam. Try changing the index in cv2.VideoCapture()")

current_emotion = "neutral"

# 🎭 Emotion tips
emotion_tips = {
    "happy": "Keep smiling and spread the joy!",
    "sad": "It's okay to feel sad. Try talking to a friend.",
    "angry": "Take a deep breath and stay calm.",
    "fear": "Face your fears slowly. You're stronger than you think.",
    "surprise": "Enjoy the surprises life gives you!",
    "disgust": "Try to change your environment or distract yourself.",
    "neutral": "Stay mindful and focused."
}

# 💬 Offline AI chatbot logic
def get_offline_reply(user_msg):
    user_msg = user_msg.lower()

    # Basic conversational logic
    if any(word in user_msg for word in ["hi", "hello", "hey"]):
        return "👋 Hello! I'm your AI buddy. How are you feeling today?"

    if "how are you" in user_msg:
        return "😊 I'm doing great and always here to support you!"

    if "who are you" in user_msg or "what are you" in user_msg:
        return "🤖 I'm an offline AI assistant who understands your emotions and cheers you up!"

    if "thank" in user_msg:
        return "🙏 You're always welcome! Stay strong!"

    if "bye" in user_msg or "goodbye" in user_msg:
        return "👋 Goodbye! Come back anytime you need a boost!"

    if any(word in user_msg for word in ["sad", "depressed", "unhappy"]):
        return "😢 I'm here for you. Even the darkest night will end and the sun will rise."

    if any(word in user_msg for word in ["happy", "joy", "excited"]):
        return "😄 That's awesome! Keep shining and enjoying life!"

    if any(word in user_msg for word in ["angry", "mad", "furious"]):
        return "😠 Breathe in, breathe out. You’re doing great. Let’s redirect that energy!"

    if any(word in user_msg for word in ["scared", "fear", "afraid"]):
        return "😨 It's okay to feel scared. Every step you take makes you braver."

    if any(word in user_msg for word in ["surprise", "shocked"]):
        return "😮 Life is full of surprises! Just enjoy the moment."

    if any(word in user_msg for word in ["disgust", "gross"]):
        return "🤢 Hmm, maybe it’s time for something refreshing or calming!"

    if any(word in user_msg for word in ["motivate", "help", "tip", "encourage"]):
        return "💡 You’re capable of amazing things. Keep going, I believe in you!"

    # Emotion fallback
    emotion_based = {
        "happy": "😄 You seem happy! Keep that positive energy alive!",
        "sad": "😢 You look a little down. Want to talk about it?",
        "angry": "😠 Try listening to some calm music or taking a short walk.",
        "fear": "😨 I know things can be scary, but you’re not alone.",
        "surprise": "😮 Life brings surprises – stay curious!",
        "disgust": "🤢 Let’s think about something peaceful and uplifting.",
        "neutral": "😐 I'm always here if you need to chat or smile!"
    }

    return emotion_based.get(current_emotion, "🤖 I'm your motivational buddy! Tell me how you're feeling.")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    def gen():
        global current_emotion
        while True:
            success, frame = camera.read()
            if not success:
                print("⚠️ Failed to read from camera.")
                break

            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                result = DeepFace.analyze(rgb_frame, actions=["emotion"], enforce_detection=False)
                if result and isinstance(result, list):
                    emotion = result[0].get("dominant_emotion", "neutral")
                else:
                    emotion = "neutral"
                current_emotion = emotion
            except Exception as e:
                print(f"⚠️ Emotion detection error: {e}")
                current_emotion = "neutral"

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/emotion')
def emotion():
    tip = emotion_tips.get(current_emotion, "")
    return jsonify({'emotion': current_emotion, 'tip': tip})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    if not msg:
        return jsonify({"response": "🤖 Say something, please!"})
    reply = get_offline_reply(msg)
    return jsonify({"response": reply})

if __name__ == '__main__':
    print("✅ Offline AI Chat Ready. Flask app is running.")
    app.run(debug=True)
