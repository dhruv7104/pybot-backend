import tkinter as tk
from tkinter import scrolledtext
from transformers import AutoModelForCausalLM, AutoTokenizer
from fuzzywuzzy import fuzz
from textblob import TextBlob
import torch
import requests
import random

# === Core Logic ===
def get_response(user_input):
    user_input = user_input.strip().lower()
    print(f"[DEBUG] Raw input: '{user_input}'")

    if len(user_input) < 2:
        return "Can you please clarify that? 😊"

    # Basic replies
    greetings = ["hi", "hello", "hey", "hii", "heyy"]
    if user_input in greetings:
        return "Hey there! 😊 What would you like to talk about?"

    if user_input in ["how are you", "how r u", "how you doing"]:
        return "I'm doing great — thanks for asking! 😊"

    if match_fuzzy(user_input, ["your name", "what is your name", "who are you"]):
        return "I'm PyBot – your smart assistant powered by AI."

    if match_fuzzy(user_input, ["bye", "goodbye", "see you"]):
        return "See you soon! 👋 Have a great day!"

    # Gym-specific logic
    if match_fuzzy(user_input, ["what to train", "which body part", "gym today"]):
        options = ["Chest 💪", "Back and Biceps 🔁", "Leg day 🦵", "Shoulders & Abs 💥", "Cardio 🏃‍♂️"]
        return f"How about: {random.choice(options)}"

    # Spelling correction
    if len(user_input.split()) < 3:
        corrected_input = correct_spelling(user_input)
        print(f"[DEBUG] Corrected input: '{corrected_input}'")
    else:
        corrected_input = user_input

    # Use Google (SerpAPI)
    google_snippet = fetch_google_snippet(corrected_input)
    if google_snippet:
        print("[DEBUG] Google snippet found.")
        return google_snippet

    # Fallback to DialoGPT
    print("[DEBUG] Falling back to AI generation.")
    return generate_ai_response(corrected_input)
