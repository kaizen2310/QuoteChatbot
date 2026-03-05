import random
import json
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load quotes from JSON (path relative to this file)
QUOTES_FILE = os.path.join(os.path.dirname(__file__), "../quotes/quotes_data.json")

with open(QUOTES_FILE, "r") as f:
    ALL_QUOTES = json.load(f)


def get_random_quote(category: str) -> str:
    quotes = ALL_QUOTES.get(category, [])
    if quotes:
        return random.choice(quotes)
    return "Every day is a new beginning. Make the most of it! 🌅"


class ActionGiveMotivationQuote(Action):
    def name(self) -> Text:
        return "action_give_motivation_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quote = get_random_quote("motivation")
        dispatcher.utter_message(text=f"💪 {quote}")
        return []


class ActionGiveInspirationQuote(Action):
    def name(self) -> Text:
        return "action_give_inspiration_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quote = get_random_quote("inspiration")
        dispatcher.utter_message(text=f"✨ {quote}")
        return []


class ActionGiveSuccessQuote(Action):
    def name(self) -> Text:
        return "action_give_success_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quote = get_random_quote("success")
        dispatcher.utter_message(text=f"🏆 {quote}")
        return []


class ActionGiveLoveQuote(Action):
    def name(self) -> Text:
        return "action_give_love_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quote = get_random_quote("love")
        dispatcher.utter_message(text=f"❤️ {quote}")
        return []


class ActionGiveHumorQuote(Action):
    def name(self) -> Text:
        return "action_give_humor_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        quote = get_random_quote("humor")
        dispatcher.utter_message(text=f"😄 {quote}")
        return []
