# 🤖 AI-Powered YouTube Spam Bot Detector with Validation

This project is an AI-powered YouTube spam bot detector that now includes a validation step to more accurately identify spam channels, including adult content, crypto scams, and general spam. It uses the YouTube Data API and Groq AI for detection and validation.

## ✨ Features

- **AI-Powered Detection:** Uses Groq's LLaMA 3 model to analyze channel data and identify potential spam bots.
- **Bot Validation:** Implements an additional AI-powered validation step to confirm if a detected channel is definitively a spam bot, reducing false positives.
- **Multi-Type Detection:** Capable of detecting various types of spam, including:
  - Adult content promotion (OnlyFans, webcam, etc.)
  - Crypto and financial scams (free Bitcoin, generators, hacks)
  - General spam (fake accounts, sub4sub, suspicious engagement)
  - UTTP/raid bots
- **Real-Time Logging:** Detected bots are logged to a text file (`detected_bots_log.txt`) in real-time.
- **Persistent Storage:** Final detected bots are saved to a JSON file (`ai_detected_spam_bots.json`).

## 📋 Requirements

- Python 3.8+
- A YouTube Data API v3 key
- A Groq API key

## ⚙️ Installation

1.  **Clone the repository or download the source code:**

    ```bash
    # If you have git installed
    git clone https://github.com/your-username/youtube-spam-bot-detector.git
    cd youtube-spam-bot-detector
    
    # If you downloaded a zip file, extract it and navigate into the directory
    ```

2.  **Create and activate a Python virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install google-api-python-client groq
    ```

## 🚀 Usage

1.  **Open `ai_spam_detector_groq.py`** in a text editor.

2.  **Replace the placeholder API keys** with your actual keys:

    ```python
    YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your YouTube Data API v3 key
    GROQ_API_KEY = "YOUR_GROQ_API_KEY"      # Replace with your Groq API key
    ```

3.  **Run the script:**

    ```bash
    source venv/bin/activate
    python ai_spam_detector_groq.py
    ```

4.  **Monitor the output** in your terminal. Detected bots will be printed to the console and appended to `detected_bots_log.txt`.

5.  **After the script completes** (or stops due to API quota limits), a summary of detected bots will be saved to `ai_detected_spam_bots.json`.

## 🔧 How It Works

1.  **Data Collection:** The script uses the YouTube Data API v3 to search for channels based on a predefined list of spam-related keywords.
2.  **Initial AI Analysis:** For each channel found, the script sends the channel's metadata (title, description, stats) to the Groq API for an initial AI analysis to determine if it's a potential spam bot.
3.  **Bot Validation:** If the initial AI analysis flags a channel as a potential spam bot, an additional AI call is made to the Groq API with a more specific prompt to definitively validate if the channel is a spam bot. This step helps to reduce false positives.
4.  **Logging and Storage:** Only channels confirmed as spam bots after the validation step are logged to `detected_bots_log.txt` and included in the final `ai_detected_spam_bots.json` file.

## ⚠️ Disclaimer

- This tool is for educational and research purposes only.
- Automated reporting of channels violates YouTube's Terms of Service. Always manually review and report channels through YouTube's official reporting system.
- The accuracy of the AI detection depends on the model and the data provided. Some legitimate channels may be flagged as spam (false positives), and some spam bots may be missed (false negatives).
- Use of the YouTube Data API is subject to quotas and limitations. If you run out of quota, the application will stop fetching new data.


