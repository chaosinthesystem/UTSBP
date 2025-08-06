import sys
import os
import json
import time
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from groq import Groq

# API Keys (These will be replaced by the user)
YOUTUBE_API_KEY = ""
GROQ_API_KEY = ""

# Initialize APIs
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

# Search queries for different types of spam bots
SEARCH_QUERIES = [
    "OnlyFans free", "webcam girls", "porn telegram", "free bitcoin", "bitcoin generator",
    "crypto hack", "free money", "spam account", "fake account", "click link bio",
    "free followers", "sub4sub", "follow back", "spam bot", "UTTP raid", "UTTP spam", "UTTP destroy"
]

def analyze_with_ai(channel_data):
    """Use Groq AI to analyze if a channel is a spam bot"""
    prompt = f"""
    Analyze this YouTube channel and determine if it\'s a spam bot. Consider:
    - Channel title: {channel_data["title"]}
    - Description: {channel_data["description"]}
    - Subscriber count: {channel_data["subscriber_count"]}
    - Video count: {channel_data["video_count"]}
    - View count: {channel_data["view_count"]}
    
    Look for signs of:
    1. Adult content promotion (OnlyFans, webcam, explicit content)
    2. Crypto/financial scams (free Bitcoin, generators, hacks)
    3. General spam patterns (fake accounts, sub4sub, suspicious engagement)
    4. UTTP/raid bots

    Respond with JSON only:
    {{
        "is_spam_bot": true/false,
        "confidence": 0.0-1.0,
        "bot_type": "adult_content" | "crypto_scam" | "general_spam" | "uttp_bot",
        "reasoning": "brief explanation",
        "risk_level": "low" | "medium" | "high"
    }}
    """

    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )

        ai_response = response.choices[0].message.content.strip()
        # Extract JSON from response
        start_idx = ai_response.find("{")
        end_idx = ai_response.rfind("}") + 1
        json_str = ai_response[start_idx:end_idx]

        return json.loads(json_str)
    except Exception as e:
        print(f"AI analysis error: {e}")
        return None

def validate_bot(channel_data):
    """Perform an additional validation check on a potential bot channel."""
    # This is a placeholder for more sophisticated validation logic.
    # For now, we\'ll use a simple heuristic: if a channel has very few videos
    # but a disproportionately high number of views, it might be a bot.
    # Or, we could use another AI call with a more specific prompt.

    # Example heuristic validation:
    if channel_data.get("video_count", 0) < 5 and channel_data.get("view_count", 0) > 10000:
        return True, "Heuristic: Very few videos with high views."

    # Example AI-based validation (more robust):
    validation_prompt = f"""
    Re-evaluate this YouTube channel for spam bot characteristics. Focus on subtle signs of automation, engagement manipulation, or deceptive content.
    - Channel title: {channel_data["title"]}
    - Description: {channel_data["description"]}
    - Subscriber count: {channel_data["subscriber_count"]}
    - Video count: {channel_data["video_count"]}
    - View count: {channel_data["view_count"]}
    - Initial AI analysis: {channel_data.get("ai_analysis", {}).get("reasoning", "N/A")}

    Is this channel definitively a spam bot? Respond with JSON only:
    {{
        "is_valid_bot": true/false,
        "validation_reasoning": "brief explanation"
    }}
    """
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": validation_prompt}],
            temperature=0.1,
            max_tokens=500
        )
        validation_response = response.choices[0].message.content.strip()
        start_idx = validation_response.find("{")
        end_idx = validation_response.rfind("}") + 1
        json_str = validation_response[start_idx:end_idx]
        validation_result = json.loads(json_str)
        return validation_result.get("is_valid_bot", False), validation_result.get("validation_reasoning", "AI validation.")
    except Exception as e:
        print(f"Validation AI error: {e}")
        return False, f"Validation failed: {e}"

def search_and_analyze():
    """Search for channels and analyze them with AI"""
    detected_bots = []
    total_analyzed = 0

    # Clear previous log file
    if os.path.exists("detected_bots_log.txt"):
        os.remove("detected_bots_log.txt")

    for query in SEARCH_QUERIES:
        print(f"🔍 Searching for: \'{query}\'")
        print("=" * 60)

        try:
            search_response = youtube.search().list(
                q=query,
                type="channel",
                part="snippet",
                maxResults=10
            ).execute()

            for item in search_response["items"]:
                channel_id = item["id"]["channelId"]

                # Get detailed channel info
                channel_response = youtube.channels().list(
                    part="snippet,statistics",
                    id=channel_id
                ).execute()

                if channel_response["items"]:
                    channel = channel_response["items"][0]
                    channel_data = {
                        "title": channel["snippet"]["title"],
                        "channel_id": channel_id,
                        "url": f"https://www.youtube.com/channel/{channel_id}",
                        "description": channel["snippet"].get("description", ""),
                        "subscriber_count": int(channel["statistics"].get("subscriberCount", 0)),
                        "video_count": int(channel["statistics"].get("videoCount", 0)),
                        "view_count": int(channel["statistics"].get("viewCount", 0)),
                        "found_via_query": query
                    }

                    total_analyzed += 1
                    print(f"🤖 Analyzing channel {total_analyzed}: {channel_data['title']}...")

                    # Analyze with AI
                    ai_analysis = analyze_with_ai(channel_data)

                    if ai_analysis and ai_analysis.get("is_spam_bot"):
                        channel_data["ai_analysis"] = ai_analysis
                        
                        # Perform validation
                        is_valid_bot, validation_reasoning = validate_bot(channel_data)
                        channel_data["validation"] = {
                            "is_valid_bot": is_valid_bot,
                            "reasoning": validation_reasoning
                        }

                        if is_valid_bot:
                            detected_bots.append(channel_data)

                            print(f"🚨 SPAM BOT DETECTED #{len(detected_bots)}: {channel_data['title']}")
                            print(f"   Type: {ai_analysis['bot_type']}")
                            print(f"   Confidence: {ai_analysis['confidence']:.2f}")
                            print(f"   Risk: {ai_analysis['risk_level']}")
                            print(f"   Reasoning: {ai_analysis['reasoning']}")
                            print(f"   Validation: {validation_reasoning}")
                            print(f"   URL: {channel_data['url']}")
                            print(f"   Stats: {channel_data['subscriber_count']} subs, {channel_data['video_count']} videos")
                            print("-" * 60)

                            # Save to log file
                            with open("detected_bots_log.txt", "a") as f:
                                f.write(json.dumps(channel_data) + '\n')
                        else:
                            print(f"⚠️ Potential bot {channel_data['title']} failed validation: {validation_reasoning}")

                    time.sleep(1)  # Rate limiting

        except HttpError as e:
            print(f"Error searching for \'{query}\': {e}")
            if "quotaExceeded" in str(e):
                print("YouTube API quota exceeded. Stopping...")
                break

    print(f"🎯 AI-POWERED SEARCH COMPLETE!")
    print(f"Total channels analyzed: {total_analyzed}")
    print(f"Spam bots detected (after validation): {len(detected_bots)}")

    # Save final results
    with open("ai_detected_spam_bots.json", "w") as f:
        json.dump(detected_bots, f, indent=2)

    return detected_bots

if __name__ == "__main__":
    search_and_analyze()

