import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import pyttsx3
from gtts import gTTS
import os
import uuid

# Initialize translator and TTS engine
translator = Translator()
tts_engine = pyttsx3.init()

# Get language codes and names
language_choices = list(LANGUAGES.values())
language_map = {v: k for k, v in LANGUAGES.items()}

# Speak the given text
def speak_text(text, lang):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = f"temp_{uuid.uuid4()}.mp3"
        tts.save(filename)
        os.system(f"start {filename}" if os.name == 'nt' else f"afplay {filename}")
    except Exception as e:
        messagebox.showerror("TTS Error", f"Could not play speech.\n{e}")

# Translate text
def translate_text():
    source_lang = language_map[source_combo.get()]
    target_lang = language_map[target_combo.get()]
    input_text = source_text.get("1.0", tk.END).strip()

    if not input_text:
        messagebox.showwarning("Input Required", "Please enter text to translate.")
        return

    try:
        translated = translator.translate(input_text, src=source_lang, dest=target_lang)
        target_text.delete("1.0", tk.END)
        target_text.insert(tk.END, translated.text)
    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred:\n{e}")

# Copy translation to clipboard
def copy_translation():
    text = target_text.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Translation copied to clipboard!")

# Paste into input box
def paste_input():
    pasted = root.clipboard_get()
    source_text.insert(tk.END, pasted)

# Text-to-speech for translated text
def tts_target():
    lang_code = language_map[target_combo.get()]
    text = target_text.get("1.0", tk.END).strip()
    if text:
        speak_text(text, lang_code)
    else:
        messagebox.showwarning("Empty", "No translated text to read.")

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("🌍 Language Translator")
root.geometry("700x400")
root.resizable(False, False)

# Labels
tk.Label(root, text="Source Language").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Target Language").grid(row=0, column=2, padx=10, pady=10)

# Dropdowns
source_combo = ttk.Combobox(root, values=language_choices, state='readonly', width=30)
source_combo.grid(row=0, column=1)
source_combo.set("english")

target_combo = ttk.Combobox(root, values=language_choices, state='readonly', width=30)
target_combo.grid(row=0, column=3)
target_combo.set("hindi")

# Text Areas
source_text = tk.Text(root, height=8, width=40, wrap='word')
source_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

target_text = tk.Text(root, height=8, width=40, wrap='word')
target_text.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

# Buttons
tk.Button(root, text="Translate", width=20, command=translate_text).grid(row=2, column=1, pady=10)
tk.Button(root, text="Copy Translation", command=copy_translation).grid(row=2, column=2, pady=10)
tk.Button(root, text="Paste", command=paste_input).grid(row=3, column=0, pady=10)
tk.Button(root, text="Speak Output", command=tts_target).grid(row=3, column=3, pady=10)

root.mainloop()
