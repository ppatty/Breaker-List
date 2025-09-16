const quizData = [
  {
    question: "Which spirit forms the base of a classic Mojito?",
    options: ["White rum", "Gin", "Tequila", "Vodka"],
    answerIndex: 0
  },
  {
    question: "What ingredient adds bitterness to a traditional Old Fashioned?",
    options: ["Orange juice", "Angostura bitters", "Simple syrup", "Vermouth"],
    answerIndex: 1
  },
  {
    question: "Which cocktail combines gin, sweet vermouth, and Campari in equal parts?",
    options: ["Negroni", "Manhattan", "Moscow Mule", "Mai Tai"],
    answerIndex: 0
  },
  {
    question: "What citrus component is essential in a Margarita?",
    options: ["Lemon juice", "Grapefruit juice", "Lime juice", "Orange juice"],
    answerIndex: 2
  },
  {
    question: "A Whiskey Sour is often finished with which frothy ingredient?",
    options: ["Egg white", "Heavy cream", "Coconut milk", "Tonic water"],
    answerIndex: 0
  },
  {
    question: "Which garnish is most traditional for a Singapore Sling?",
    options: ["Celery stalk", "Mint sprig", "Cherry and pineapple", "Cucumber wheel"],
    answerIndex: 2
  }
];

const leaderboardKey = "cocktailQuizLeaderboard";

let currentQuestionIndex = 0;
let selectedOptionIndex = null;
let score = 0;
let quizStartedAt = null;
let elapsedSeconds = 0;

const startScreen = document.getElementById("start-screen");
const quizScreen = document.getElementById("quiz-screen");
const resultScreen = document.getElementById("result-screen");
const startButton = document.getElementById("start-quiz");
const nextButton = document.getElementById("next-question");
const playAgainButton = document.getElementById("play-again");
const submitButton = document.getElementById("submit-score");
const resetButton = document.getElementById("reset-leaderboard");

const questionText = document.getElementById("question-text");
const optionsContainer = document.getElementById("options-container");
const progressText = document.getElementById("progress-text");
const feedback = document.getElementById("feedback");
const scoreSummary = document.getElementById("score-summary");
const timeSummary = document.getElementById("time-summary");
const resultMessage = document.getElementById("result-message");
const playerNameInput = document.getElementById("player-name");
const leaderboardList = document.getElementById("leaderboard-list");

startButton.addEventListener("click", startQuiz);
nextButton.addEventListener("click", handleNextQuestion);
playAgainButton.addEventListener("click", resetToStart);
submitButton.addEventListener("click", submitScore);
resetButton.addEventListener("click", resetLeaderboard);

refreshLeaderboard();

function startQuiz() {
  score = 0;
  currentQuestionIndex = 0;
  selectedOptionIndex = null;
  quizStartedAt = Date.now();
  elapsedSeconds = 0;

  startScreen.classList.add("hidden");
  resultScreen.classList.add("hidden");
  quizScreen.classList.remove("hidden");
  nextButton.disabled = true;
  feedback.textContent = "";

  renderQuestion();
}

function renderQuestion() {
  const questionData = quizData[currentQuestionIndex];
  questionText.textContent = questionData.question;
  progressText.textContent = `Question ${currentQuestionIndex + 1} of ${
    quizData.length
  }`;

  optionsContainer.innerHTML = "";
  selectedOptionIndex = null;
  nextButton.disabled = true;

  questionData.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "option-button";
    button.textContent = option;
    button.dataset.index = index;
    button.addEventListener("click", () => selectOption(button, index));
    optionsContainer.appendChild(button);
  });
}

function selectOption(button, index) {
  selectedOptionIndex = index;
  Array.from(optionsContainer.children).forEach((child) =>
    child.classList.remove("selected")
  );
  button.classList.add("selected");
  nextButton.disabled = false;
  feedback.textContent = "";
}

function handleNextQuestion() {
  if (selectedOptionIndex === null) {
    feedback.textContent = "Please choose an answer to continue.";
    return;
  }

  const questionData = quizData[currentQuestionIndex];
  if (selectedOptionIndex === questionData.answerIndex) {
    score += 1;
  }

  currentQuestionIndex += 1;

  if (currentQuestionIndex < quizData.length) {
    renderQuestion();
  } else {
    finishQuiz();
  }
}

function finishQuiz() {
  elapsedSeconds = Math.round((Date.now() - quizStartedAt) / 1000);
  quizScreen.classList.add("hidden");
  resultScreen.classList.remove("hidden");

  scoreSummary.textContent = `You nailed ${score} out of ${quizData.length} cocktail questions.`;
  timeSummary.textContent = `Completed in ${elapsedSeconds} second${
    elapsedSeconds === 1 ? "" : "s"
  }.`;
  resultMessage.textContent = "";
  submitButton.disabled = false;
  playerNameInput.value = "";
  playerNameInput.focus({ preventScroll: true });

  refreshLeaderboard();
}

function resetToStart() {
  resultScreen.classList.add("hidden");
  quizScreen.classList.add("hidden");
  startScreen.classList.remove("hidden");
  resultMessage.textContent = "";
  feedback.textContent = "";
}

function submitScore() {
  const name = playerNameInput.value.trim();
  if (!name) {
    resultMessage.textContent = "Please enter your name before saving.";
    playerNameInput.focus();
    return;
  }

  const leaderboard = loadLeaderboard();
  const entry = {
    name,
    score,
    total: quizData.length,
    time: elapsedSeconds,
    timestamp: new Date().toISOString()
  };

  leaderboard.push(entry);
  leaderboard.sort((a, b) => {
    if (b.score !== a.score) {
      return b.score - a.score;
    }
    return a.time - b.time;
  });

  const trimmed = leaderboard.slice(0, 20);
  localStorage.setItem(leaderboardKey, JSON.stringify(trimmed));

  resultMessage.textContent = "Score saved!";
  submitButton.disabled = true;
  refreshLeaderboard();
}

function loadLeaderboard() {
  const stored = localStorage.getItem(leaderboardKey);
  if (!stored) {
    return [];
  }

  try {
    const parsed = JSON.parse(stored);
    if (Array.isArray(parsed)) {
      return parsed;
    }
  } catch (error) {
    console.error("Unable to parse leaderboard", error);
  }
  return [];
}

function refreshLeaderboard() {
  const leaderboard = loadLeaderboard();
  leaderboardList.innerHTML = "";

  if (leaderboard.length === 0) {
    const emptyState = document.createElement("li");
    emptyState.textContent = "No scores yet — claim the first round!";
    leaderboardList.appendChild(emptyState);
    return;
  }

  leaderboard.forEach((entry, index) => {
    const item = document.createElement("li");

    const rank = document.createElement("span");
    rank.className = "rank";
    rank.textContent = `#${index + 1}`;

    const name = document.createElement("span");
    name.className = "name";
    name.textContent = entry.name;

    const score = document.createElement("span");
    score.className = "score";
    score.textContent = `${entry.score}/${entry.total}`;

    const time = document.createElement("span");
    time.className = "time";
    time.textContent = `${entry.time}s`;

    item.append(rank, name, score, time);
    leaderboardList.appendChild(item);
  });
}

function resetLeaderboard() {
  if (confirm("Clear all saved results from this device?")) {
    localStorage.removeItem(leaderboardKey);
    refreshLeaderboard();
    resultMessage.textContent = "Leaderboard cleared.";
  }
}
