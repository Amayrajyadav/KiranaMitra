# KiranaMitra
# 🛒 KiranaMitra – AI Shop Assistant

<img width="299" height="168" alt="image" src="https://github.com/user-attachments/assets/e53a3932-5064-4b7f-9eb5-c9ae2f35a4a2" />

**Description:**  
KiranaMitra is a Streamlit-based hackathon app that lets users order items from a virtual Kirana shop via typing or voice. It generates a PDF invoice automatically.

**Features:**
- Type or speak your order (Whisper → GPT-4o mini)
- Inventory lookup & name correction
- Auto bill calculation
- Downloadable PDF invoice

**Inventory:**
- Preloaded in `inventory.csv`

🛠️ Tech Stack

- **Frontend & App:** Streamlit
- <img width="294" height="172" alt="image" src="https://github.com/user-attachments/assets/4e0086c2-5e9e-4a9d-84f9-74dbef88d75a" />

- **AI APIs:** OpenAI GPT-4o mini, Whisper
- <img width="432" height="117" alt="image" src="https://github.com/user-attachments/assets/639e4a12-d2a3-4717-8e69-ddaded754e82" />

- **Inventory Management:** CSV-based lookup
- <img width="225" height="225" alt="image" src="https://github.com/user-attachments/assets/ee5c8601-06a0-4764-9b61-67a3070f4aa2" />

- **PDF Generation:** ReportLab
- <img width="511" height="99" alt="image" src="https://github.com/user-attachments/assets/833378dc-afc0-4e6e-b762-edfb75557293" />

- **Audio Processing:** SoundDevice, SciPy
<img width="464" height="108" alt="image" src="https://github.com/user-attachments/assets/1e743a63-5ede-49e3-938e-3f24e6c0d6b0" />

** Use of APis:**
My project integrates multiple OpenAI tools to make the assistant intelligent and accessible:
Whisper API → Converts shopkeepers’ voice commands (Telugu/Hindi/English) into text
GPT-4o mini API → Parses requests, matches them with inventory, generates bills, and suggests reorders
(Future extension) Vision API → Barcode or image-based product recognition
Integration flow:
Whisper → Speech-to-text → GPT-4o mini → Inventory lookup & bill creation → PDF invoice output

**Feasibility plan **
I designed the solution to be lightweight and realistic for small shops.

Tech stack:
->Python (core logic)
->OpenAI APIs (Whisper + GPT-4o mini)
->Pandas / SQLite (inventory management)
->ReportLab (PDF invoice generation)
->Streamlit (demo UI)

Prototype plan:
1.Prepare a sample CSV with 20–50 kirana items
2.Python script: text/voice → AI parses → generates bill
3.Build a Streamlit interface for live demo
4.Export PDF bills and update stock in real time
