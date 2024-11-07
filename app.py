
# Import required libraries
import os
from groq import Groq
from transformers import pipeline
from gtts import gTTS
import streamlit as st

# Set up Groq API with your API key
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize Hugging Face Translation Models for Urdu, Arabic, and Hindi
try:
    translator_en_to_ur = pipeline("translation_en_to_ur", model="Helsinki-NLP/opus-mt-en-ur")
    translator_en_to_ar = pipeline("translation_en_to_ar", model="Helsinki-NLP/opus-mt-en-ar")
    translator_en_to_hi = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
except Exception as e:
    print("Error loading translation models:", e)

# Function to translate text into multiple languages
def translate_text_multiple_languages(text):
    translations = {}
    try:
        translations['Urdu'] = translator_en_to_ur(text)[0]['translation_text']
    except Exception as e:
        print("Error during Urdu translation:", e)
        translations['Urdu'] = "Translation not available."

    try:
        translations['Arabic'] = translator_en_to_ar(text)[0]['translation_text']
    except Exception as e:
        print("Error during Arabic translation:", e)
        translations['Arabic'] = "Translation not available."

    try:
        translations['Hindi'] = translator_en_to_hi(text)[0]['translation_text']
    except Exception as e:
        print("Error during Hindi translation:", e)
        translations['Hindi'] = "Translation not available."

    return translations

# Vocabulary Quiz Function for Multiple Languages
def vocabulary_quiz(word):
    translations = translate_text_multiple_languages(word)
    quiz_output = "Vocabulary Quiz:\n"
    for language, translation in translations.items():
        quiz_output += f"How do you say '{word}' in {language}? Answer: {translation}\n"
    return quiz_output

# Function for pronunciation using text-to-speech
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    return "response.mp3"

# Function for grammar explanations using Groq API
def get_grammar_explanation(query):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content

# Streamlit front end code
def main():
    st.title("Language Tutor Bot")
    st.subheader("Learn languages interactively with quizzes, grammar tips, and more!")
    
    # Option for vocabulary quiz in multiple languages
    st.write("\nVocabulary Quiz")
    word = st.text_input("Enter an English word for translation into Urdu, Arabic, and Hindi:")
    if word:
        quiz_response = vocabulary_quiz(word)
        st.write(quiz_response)
        # Option for grammar explanations
    st.write("\nGrammar Explanations")
    grammar_query = st.text_input("Ask about any grammar topic (e.g., past tense in English):")
    if grammar_query:
        explanation = get_grammar_explanation(grammar_query)
        st.write(explanation)

    # Option for translation practice in multiple languages
    st.write("\nTranslation Practice")
    text_to_translate = st.text_input("Enter text to translate (English to Urdu, Arabic, and Hindi):")
    if text_to_translate:
        translations = translate_text_multiple_languages(text_to_translate)
        st.write("Translations:")
        for language, translation in translations.items():
            st.write(f"{language}: {translation}")
    
    # Option for pronunciation
    st.write("\nPractice Pronunciation")
    text_to_speak = st.text_input("Enter text for pronunciation:")
    if text_to_speak:
        audio_file = speak_text(text_to_speak)
        st.audio(audio_file)

if __name__ == "__main__":
    main()
