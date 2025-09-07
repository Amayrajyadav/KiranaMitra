# -----------------------------
# KiranaMitra – Full Hackathon App
# -----------------------------

# --- Imports ---
import streamlit as st
import pandas as pd
import openai
from difflib import get_close_matches
from reportlab.pdfgen import canvas
import tempfile
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import io

# --- OpenAI API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- App Title ---
st.title("🛒 KiranaMitra – AI Shop Assistant")

# --- Load Inventory ---
@st.cache_data
def load_inventory():
    df = pd.read_csv("inventory.csv")
    df['Item Name'] = df['Item Name'].str.strip()
    df['Item Name Clean'] = df['Item Name'].str.lower().str.strip()
    return df

inventory = load_inventory()
st.subheader("Available Inventory")
st.dataframe(inventory)

# --- GPT Parsing Function (without raw output) ---
def parse_order_with_gpt(text):
    prompt = f"""
    You are an assistant. Convert this shopping text into a structured list of items and quantities.
    Text: "{text}"
    Format: JSON array of {{'item': name, 'quantity': number}}
    Only return valid JSON array. Do NOT add markdown, text, or explanations.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content

        # Clean any markdown
        cleaned = raw_output.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        import json
        return json.loads(cleaned)
    except Exception as e:
        st.error(f"Error parsing GPT output: {e}")
        return []

# --- Record Voice and Convert to Text (Whisper) ---
def record_and_transcribe(duration=5, fs=16000):
    st.info(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_wav.name, fs, recording)
    st.success("Recording complete. Transcribing...")
    with open(temp_wav.name, "rb") as f:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

# --- Order Input Area ---
st.subheader("Place Your Order")
typed_input = st.text_area("Type your order (e.g., 2 Parle-G, 1 Sunlight Soap)")
voice_input = st.button("Record Voice Order (5 sec)")

if voice_input:
    try:
        typed_input = record_and_transcribe(duration=5)
        st.text_area("Detected Order:", typed_input, height=100)

    except Exception as e:
        st.error(f"Voice input failed: {e}")

# --- Generate Bill ---
if st.button("Generate Bill"):
    order_text = typed_input.strip()
    if not order_text:
        st.warning("Please enter or record your order first.")
    else:
        parsed_order = parse_order_with_gpt(order_text)

        bill_items = []
        total = 0

        # Name corrections for common GPT variants
        name_corrections = {
            "hershey's chocolate": "Hersheys Chocolate",
            "ponds face cream": "Pond's Face Cream",
            "lays chips": "Lay's Chips",
            "maggie noodles": "Maggi Noodles",
            "tata salt": "Tata Salt",
            "sunlightsoap": "Sunlight Soap",
            "parle g": "Parle-G"
        }

        for item in parsed_order:
            name = item.get("item", "").lower().strip()
            name = name_corrections.get(name, name)
            qty = int(item.get("quantity", 0))

            matched_name = get_close_matches(name, inventory['Item Name Clean'], n=1, cutoff=0.5)
            if matched_name:
                row = inventory[inventory['Item Name Clean'] == matched_name[0]]
                price = row.iloc[0]['Price']
                amount = qty * price
                total += amount
                bill_items.append((row.iloc[0]['Item Name'], qty, price, amount))

        if bill_items:
            st.subheader("Bill Details")
            for i in bill_items:
                st.write(f"{i[0]} - Qty: {i[1]} x Price: {i[2]} = {i[3]}")
            st.write(f"**Total Amount: {total}**")

            # --- Generate PDF and make it downloadable ---
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                c = canvas.Canvas(temp_pdf.name)
                c.drawString(100, 800, "🛒 KiranaMitra Bill")
                y = 750
                for i in bill_items:
                    c.drawString(100, y, f"{i[0]} - Qty: {i[1]} x Price: {i[2]} = {i[3]}")
                    y -= 20
                c.drawString(100, y-10, f"Total Amount: {total}")
                c.save()

            with open(temp_pdf.name, "rb") as f:
                pdf_bytes = f.read()

            st.success("PDF Bill Generated!")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="KiranaMitra_Bill.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No valid items found in inventory. Check item names.")
