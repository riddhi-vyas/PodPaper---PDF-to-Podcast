import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from io import BytesIO

# Load environment variables
load_dotenv()

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
GROUP_ID = os.getenv("GROUP_ID")

# Voice IDs for speakers
HOST_VOICE_ID = "male-qn-qingse"
GUEST_VOICE_ID = "female-shaonv"


def extract_text(pdf_file) -> str:
    """Extract text from the first 2 pages of a PDF file."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        # Limit to first 2 pages
        pages_to_read = min(2, len(reader.pages))
        for i in range(pages_to_read):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting PDF text: {e}")
        return ""


def generate_script(text: str) -> list:
    """Generate a podcast script using MiniMax LLM."""
    url = "https://api.minimax.io/v1/text/chatcompletion_v2"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are a podcast script writer. Summarize the given text into an engaging dialogue between two podcasters (Host and Guest). 
The Host introduces topics and asks questions, while the Guest provides insights and explanations.
Make the conversation natural, informative, and engaging.

Return ONLY a JSON list of objects in this exact format, with no additional text or markdown:
[{"speaker": "Host", "text": "..."}, {"speaker": "Guest", "text": "..."}, ...]

Keep each speaker's text concise (1-3 sentences per turn) for better audio generation."""

    payload = {
        "model": "MiniMax-Text-01",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create a podcast script from this text:\n\n{text}"}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract the content from the response
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            
            # Clean up the content - remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # Parse the JSON
            script = json.loads(content)
            return script
        else:
            st.error("Unexpected API response format")
            return []
            
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse script JSON: {e}")
        return []


def generate_audio(text: str, voice_id: str) -> bytes:
    """Generate audio using MiniMax Text-to-Audio API."""
    import base64
    
    url = f"https://api.minimax.io/v1/t2a_v2?GroupId={GROUP_ID}"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "speech-01-hd",
        "text": text,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        # Try to extract audio data from various response formats
        audio_data = None
        
        # Format 1: data.audio (hex encoded)
        if "data" in result and "audio" in result["data"]:
            audio_data = result["data"]["audio"]
        # Format 2: audio_file
        elif "audio_file" in result:
            audio_data = result["audio_file"]
        # Format 3: direct audio field
        elif "audio" in result:
            audio_data = result["audio"]
        else:
            st.error(f"Unexpected audio API response structure: {list(result.keys())}")
            return b""
        
        if not audio_data:
            st.error("Empty audio data received from API")
            return b""
        
        # Try hex decoding first (MiniMax often returns hex-encoded audio)
        try:
            audio_bytes = bytes.fromhex(audio_data)
            return audio_bytes
        except ValueError:
            pass
        
        # Try base64 decoding with padding fix
        try:
            # Add padding if needed
            padding = 4 - (len(audio_data) % 4)
            if padding != 4:
                audio_data += "=" * padding
            audio_bytes = base64.b64decode(audio_data)
            return audio_bytes
        except Exception:
            pass
        
        # Try standard base64 decoding
        try:
            audio_bytes = base64.b64decode(audio_data)
            return audio_bytes
        except Exception as e:
            st.error(f"Failed to decode audio data: {e}")
            return b""
            
    except requests.exceptions.RequestException as e:
        st.error(f"Audio generation failed: {e}")
        return b""
    except Exception as e:
        st.error(f"Unexpected error in audio generation: {e}")
        return b""


# Streamlit UI
st.set_page_config(
    page_title="PodPaper",
    page_icon="🎧",
    layout="centered"
)

st.title("PodPaper 🎧")
st.markdown("*Transform your PDFs into engaging podcast conversations*")

# Check for API keys
if not MINIMAX_API_KEY or not GROUP_ID:
    st.warning("⚠️ Missing API configuration. Please set `MINIMAX_API_KEY` and `GROUP_ID` in your `.env` file.")
    st.code("""
# .env file format:
MINIMAX_API_KEY=your_api_key_here
GROUP_ID=your_group_id_here
    """, language="bash")
    st.stop()

st.divider()

# File uploader
uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    help="Upload a PDF file to convert into a podcast script"
)

if uploaded_file is not None:
    st.success(f"📄 Uploaded: **{uploaded_file.name}**")
    
    # Generate button
    if st.button("🎙️ Generate Podcast", type="primary", use_container_width=True):
        
        # Step 1: Extract text
        with st.spinner("📖 Extracting text from PDF..."):
            extracted_text = extract_text(uploaded_file)
        
        if not extracted_text:
            st.error("Could not extract text from the PDF. Please try a different file.")
            st.stop()
        
        # Show extracted text preview
        with st.expander("📝 Extracted Text Preview", expanded=False):
            st.text(extracted_text[:2000] + ("..." if len(extracted_text) > 2000 else ""))
        
        # Step 2: Generate script
        with st.spinner("✍️ Generating podcast script..."):
            script = generate_script(extracted_text)
        
        if not script:
            st.error("Failed to generate podcast script. Please try again.")
            st.stop()
        
        # Display the script
        st.subheader("📜 Generated Script")
        
        script_container = st.container()
        with script_container:
            for line in script:
                speaker = line.get("speaker", "Unknown")
                text = line.get("text", "")
                
                if speaker == "Host":
                    st.markdown(f"**🎤 Host:** {text}")
                else:
                    st.markdown(f"**🎧 Guest:** {text}")
        
        st.divider()
        
        # Step 3: Generate audio
        st.subheader("🔊 Audio Clips")
        
        with st.spinner("🎵 Synthesizing audio..."):
            for i, line in enumerate(script):
                speaker = line.get("speaker", "Unknown")
                text = line.get("text", "")
                
                if not text:
                    continue
                
                # Select voice based on speaker
                if speaker == "Host":
                    voice_id = HOST_VOICE_ID
                    icon = "🎤"
                else:
                    voice_id = GUEST_VOICE_ID
                    icon = "🎧"
                
                st.markdown(f"**{icon} {speaker}:** *{text[:100]}{'...' if len(text) > 100 else ''}*")
                
                # Generate audio for this line
                audio_bytes = generate_audio(text, voice_id)
                
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.warning(f"Could not generate audio for line {i + 1}")
                
                st.markdown("---")
        
        st.success("✅ Podcast generation complete!")

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #888;'>Built with ❤️ using Streamlit & MiniMax AI</div>",
    unsafe_allow_html=True
)
