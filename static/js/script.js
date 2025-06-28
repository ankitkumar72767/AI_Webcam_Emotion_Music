<script>
  const audio = document.getElementById("audio");
  const emojiDisplay = document.getElementById("emoji");
  const emotionHistory = [];

  // 🔁 Emotion to Emoji mapping
  const emotionMap = {
    happy: "😄",
    sad: "😢",
    angry: "😠",
    neutral: "😐",
    surprise: "😮",
    fear: "😨",
    disgust: "🤢"
  };

  // 🎵 Emotion to music mapping
  const musicMap = {
    happy: "/static/music/happy.mp3",
    sad: "/static/music/sad.mp3",
    angry: "/static/music/angry.mp3",
    neutral: "/static/music/neutral.mp3",
    surprise: "/static/music/surprise.mp3",
    fear: "/static/music/fear.mp3",
    disgust: "/static/music/disgust.mp3"
  };

  let currentEmotion = "neutral";

  function fetchEmotion() {
    fetch("/emotion")
      .then(res => res.json())
      .then(data => {
        const emotion = data.emotion || "neutral";
        const tip = data.tip || "Stay positive!";
        const emoji = emotionMap[emotion] || "🙂";

        // Only update if emotion has changed
        if (emotion !== currentEmotion) {
          currentEmotion = emotion;
          emojiDisplay.textContent = emoji;

          // 🎶 Play emotion-specific music
          audio.src = musicMap[emotion] || musicMap["neutral"];
          audio.play();

          // 🕒 Update emotion history (max 5)
          emotionHistory.unshift(`${emoji} ${emotion}`);
          if (emotionHistory.length > 5) emotionHistory.pop();

          document.getElementById("emotionHistory").innerHTML =
            `<strong>🕒 Last Emotions:</strong> ` + emotionHistory.join(" | ");
        }

        // 🎭 Update emotion text
        document.getElementById("emotion").innerHTML =
          `🎭 <b>Emotion:</b> ${emotion.toUpperCase()} ${emoji}`;

        // 💡 Display tip
        document.getElementById("tip").innerHTML =
          `💡 <i>${tip}</i>`;
      })
      .catch(error => {
        console.error("Error fetching emotion:", error);
      });
  }

  // 🔁 Refresh emotion every 2 seconds
  setInterval(fetchEmotion, 2000);
</script>
