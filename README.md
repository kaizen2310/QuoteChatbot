# Quotes Chatbot 

A conversational AI chatbot built with Rasa Open Source that delivers personalized quotes across five categories — motivation, inspiration, success, love, and humor — through natural language interaction.

**[Live Demo](https://quotes-chatbot.vercel.app)** · **[Report an Issue](hhttps://github.com/kaizen2310/QuoteChatbot/issues)**

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Testing](#testing)
- [Deployment](#deployment)
- [Extending the Project](#extending-the-project)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Five quote categories** — Motivation, Inspiration, Success, Love, and Humor
- **Multi-turn conversation** — Context-aware dialogue with support for follow-up requests
- **Graceful fallback** — Handles unrecognized or low-confidence input without breaking the conversation
- **Responsive web interface** — Chat UI compatible with both desktop and mobile browsers
- **Extensible design** — New quote categories can be added with minimal code changes

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| NLU Engine | Rasa Open Source | 3.6.21 |
| Custom Actions | Rasa SDK | 3.6.2 |
| Language | Python | 3.10+ |
| Frontend | HTML / CSS / JavaScript | — |

---

## Prerequisites

Ensure the following are installed before proceeding:

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kaizen2310/QuoteChatbot.git
cd QuoteChatbot
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python3.10 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
py -3.10 -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install rasa rasa-sdk
```

> Note: Rasa is approximately 500 MB. Installation typically takes 2–3 minutes.

### 4. Train the model

```bash
rasa train
```

> This generates a trained model under the `models/` directory and takes approximately 2–3 minutes.

### 5. Start the bot

Open two terminal windows:

**Terminal 1 — Action server:**
```bash
rasa run actions
```

**Terminal 2 — Interactive shell:**
```bash
rasa shell
```

You can now type messages such as `"hi"` or `"I need motivation"` to interact with the bot.

**Optional — Enable REST API and web UI:**
```bash
rasa run --enable-api --cors "*"
```
Then open `frontend/index.html` in a browser to use the chat interface.

---

## Project Structure

```
QuoteChatbot/
├── data/
│   ├── nlu.yml              # Intent training examples
│   ├── stories.yml          # Multi-turn conversation flows
│   └── rules.yml            # Hard conversation rules
├── actions/
│   └── actions.py           # Custom action definitions
├── quotes/
│   └── quotes_data.json     # Quote database (5 categories)
├── frontend/
│   └── index.html           # Web chat interface
├── domain.yml               # Bot configuration (intents, actions, responses)
├── config.yml               # NLU pipeline and dialogue policies
├── credentials.yml          # Channel configuration
├── endpoints.yml            # Action server endpoint
├── models/                  # Trained model artifacts (auto-generated)
├── requirements.txt
└── .gitignore
```

---

## Architecture

### NLU Pipeline

Incoming messages are processed through the following pipeline, defined in `config.yml`:

```
WhitespaceTokenizer
→ RegexFeaturizer + LexicalSyntacticFeaturizer
→ CountVectorsFeaturizer (word-level + character n-grams)
→ DIETClassifier         (intent classification)
→ ResponseSelector       (response selection)
→ FallbackClassifier     (low-confidence handling)
```

**Example flow:**
```
User:   "motivate me"
Intent: request_motivation_quote  (confidence: 0.98)
Action: action_give_motivation_quote
Output: "Push yourself, because no one else is going to do it for you."
```

### Dialogue Policies

| Policy | Role |
|--------|------|
| `MemoizationPolicy` | Reproduces exact patterns from training stories |
| `RulePolicy` | Enforces hard rules (greet, goodbye, fallback) |
| `UnexpecTEDIntentPolicy` | Handles intents appearing in unexpected context |
| `TEDPolicy` | Generalized learned policy for flexible dialogue |

### Custom Actions

Each quote category has a dedicated action class in `actions/actions.py`:

| Action | Category |
|--------|----------|
| `ActionGiveMotivationQuote` | Motivation |
| `ActionGiveInspirationQuote` | Inspiration |
| `ActionGiveSuccessQuote` | Success |
| `ActionGiveLoveQuote` | Love |
| `ActionGiveHumorQuote` | Humor |

Each action retrieves a random quote from `quotes/quotes_data.json` and dispatches it to the user.

### Training Data

| File | Contents |
|------|---------|
| `data/nlu.yml` | 10 intents, 8–15 examples each (90+ total) |
| `data/stories.yml` | 5 multi-turn conversation stories |
| `data/rules.yml` | 3 hard rules: greet, goodbye, fallback |

---

## Testing

### Manual testing

```bash
rasa shell
```

| Input | Expected Output |
|-------|----------------|
| `hi` | Greeting response |
| `motivate me` | Motivation quote |
| `inspire me` | Inspiration quote |
| `success quotes` | Success quote |
| `love quote` | Love quote |
| `make me laugh` | Humor quote |
| `yes` / `one more` | Another quote in the same category |
| `bye` | Goodbye response |
| `xyz123blah` | Fallback response |

### Automated story tests

```bash
rasa test --stories tests/test_stories.yml
```

### NLU cross-validation

```bash
rasa test nlu --cross-validation
```

Outputs intent classification accuracy metrics and highlights areas where training data may need improvement.

---

## Deployment

To host this project on any server or cloud platform:

1. Provision a server with Python 3.10+ and install the dependencies:
   ```bash
   pip install rasa rasa-sdk
   ```
2. Train the model and start the action server and Rasa API:
   ```bash
   rasa train
   rasa run actions &
   rasa run --enable-api --cors "*" --port 5005
   ```
3. Update `RASA_URL` in `frontend/index.html` to point to your server's public address:
   ```javascript
   const RASA_URL = "https://your-server-domain.com/webhooks/rest/webhook";
   ```
4. Serve the `frontend/` directory via any static file host or web server.

Ensure port `5005` is open and CORS is correctly configured if the frontend is served from a different domain.

---

## Extending the Project

### Adding a new quote category

**1. Register the intent in `domain.yml`:**
```yaml
intents:
  - request_wisdom_quote
```

**2. Add training examples to `data/nlu.yml`:**
```yaml
- intent: request_wisdom_quote
  examples: |
    - share some wisdom
    - give me a philosophical quote
    - wise sayings
    - something thought-provoking
```

**3. Define an action class in `actions/actions.py`:**
```python
class ActionGiveWisdomQuote(Action):
    def name(self) -> Text:
        return "action_give_wisdom_quote"

    def run(self, dispatcher, tracker, domain):
        quote = get_random_quote("wisdom")
        dispatcher.utter_message(text=f"🧙 {quote}")
        return []
```

**4. Add quotes to `quotes/quotes_data.json`:**
```json
{
  "wisdom": [
    "The only true wisdom is knowing you know nothing.",
    "In the middle of difficulty lies opportunity."
  ]
}
```

**5. Retrain the model:**
```bash
rasa train
```

> To add more quotes to an existing category, edit `quotes_data.json` directly — no retraining is required.

### Improving NLU accuracy

- Add 5–10 varied examples per intent in `data/nlu.yml`
- Write additional stories for edge cases in `data/stories.yml`
- Adjust the `FallbackClassifier` threshold in `config.yml` to tune sensitivity
- Run `rasa test nlu` after each change to track improvements

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'rasa'`**
```bash
pip install rasa rasa-sdk
```

**Port 5055 already in use (Windows)**
```powershell
Get-NetTCPConnection -LocalPort 5055
Stop-Process -Id [PID] -Force
```

**Web interface returns a network error**
- Confirm the Rasa server is running on port 5005
- Verify `RASA_URL` in `index.html` points to the correct address
- Confirm Rasa was started with the `--cors "*"` flag
- Open browser DevTools (F12 → Console) to inspect the exact error

**Incorrect quote category returned**

Add more diverse training examples for the affected intent in `data/nlu.yml` and retrain.

**Emoji characters display incorrectly**

Ensure UTF-8 encoding is declared in `frontend/index.html`:
```html
<meta charset="UTF-8">
```

---

## Resources

- [Rasa Documentation](https://rasa.com/docs/)
- [Rasa Community Forum](https://forum.rasa.com/)
- [NLU Training Best Practices](https://rasa.com/docs/rasa/nlu-only/)

---

## License

This project is licensed under the [MIT License](https://github.com/kaizen2310/QuoteChatbot/blob/main/LICENSE).

---

*Maintained by [Shreeparth Torawane](https://github.com/kaizen2310)*
