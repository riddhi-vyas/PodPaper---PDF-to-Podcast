# PodPaper 🎧 | Turn Documents into Podcasts

![Build Status](https://img.shields.io/badge/Status-Hackathon_Project-blue)
![Event](https://img.shields.io/badge/Event-AI_Valley_Build_What_You_Love-ff69b4)
![Tags](https://img.shields.io/badge/Tags-WomenInTech_GenerativeAI_MiniMax-purple)

**PodPaper** is an AI-powered tool that instantly transforms static PDF documents into engaging, two-person podcast episodes. Built for the **AI Valley "Build What You Love" Hackathon**, it leverages **MiniMax**'s advanced audio generation to make learning on the go effortless.

## 🚀 The Problem
We all have stacks of research papers, reports, and articles we need to read but struggle to find the focused time for. Reading dense text on screens is exhausting and passive.

## 💡 The Solution
PodPaper converts written content into a lively audio dialogue between a "Host" and a "Guest." Instead of reading, you can listen to a natural conversation about your document while commuting, working out, or cooking.

## ✨ Features
* **📄 PDF Text Extraction:** Automatically extracts and processes text from uploaded PDF documents.
* **🤖 AI Script Generation:** Uses **MiniMax LLM** to analyze the content and generate a natural, educational dialogue script.
* **🗣️ Hyper-Realistic Audio:** Utilizes **MiniMax T2A (Text-to-Audio)** to synthesize distinct voices for the Host and Guest.
* **⏯️ Instant Playback:** Listen to the generated audio clips immediately within the app.
* **☁️ Cloud Native:** Deployed on **Replit** for instant access.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **AI Models:** [MiniMax](https://minimax.io/) (LLM for scripting, T2A for voice synthesis)
* **PDF Processing:** `pypdf`
* **Infrastructure:** Deployed on [Replit](https://replit.com/)

## ⚙️ Setup & Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/podpaper.git](https://github.com/yourusername/podpaper.git)
    cd podpaper
    ```

2.  **Install dependencies**
    ```bash
    pip install streamlit pypdf requests python-dotenv
    ```

3.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your MiniMax credentials:
    ```env
    MINIMAX_API_KEY=your_api_key_here
    GROUP_ID=your_group_id_here
    ```

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 🎯 Usage
1.  Open the app in your browser (usually `http://localhost:8501`).
2.  Upload a PDF document (e.g., a research paper or resume).
3.  Click **"Generate Podcast"**.
4.  Watch as the AI generates a script and synthesized audio.
5.  Press play to listen to your new podcast!

## 🏆 Hackathon Tracks & Acknowledgments
Submitted to **AI Valley: Build What You Love**.

Special thanks to:
* **AI Valley** for organizing this empowering event for women in tech.
* **MiniMax** for providing the incredible Voice and LLM APIs that power this app.
* **Replit** & **Runloop** for the seamless development and deployment infrastructure.

**Tags:** `#WomenInTech` `#AIValley` `#MiniMax` `#GenerativeAI` `#BuildWhatYouLove`

## 👥 Authors
* **Riddhi Vyas** - *GenAI Engineer & Data Scientist*
* **Mahak Gupta** - *Team Member*

---
*Built with ❤️ in San Francisco.*
