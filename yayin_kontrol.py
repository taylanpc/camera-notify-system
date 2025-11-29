import os
import requests
from googleapiclient.discovery import build

# GitHub Secrets'tan gizli bilgileri çek
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

def get_live_stream_link(api_key, channel_id):
    """Kanalda aktif liste dışı yayının linkini çeker."""
    try:
        # Hata kontrolü: Anahtarların mevcut olduğundan emin olun
        if not api_key or not channel_id:
            print("Hata: API Anahtarı veya Kanal ID'si eksik.")
            return None

        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Sadece canlı yayınları arıyoruz
        search_response = youtube.search().list(
            channelId=channel_id,
            type='video',
            part='snippet',
            maxResults=1
        ).execute()

        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            # Liste dışı yayın linkini oluşturur
            live_link = f"https://youtu.be/{video_id}" 
            return live_link
        
        return None
    except Exception as e:
        # Hata olursa loglama yapın
        print(f"YouTube API Hatası: {e}")
        return None

def send_discord_notification(webhook_url, link):
    """Çekilen linki Discord Webhook üzerinden gönderir."""
    if not link:
        return 

    # Hata kontrolü: Webhook URL'sinin mevcut olduğundan emin olun
    if not webhook_url:
        print("Hata: Discord Webhook URL'si eksik.")
        return

    payload = {
        "content": f"🚨 **GÜVENLİK KAMERASI AKTİF** 🚨\n🎥 Yeni Liste Dışı Yayın Başladı!\n**Link:** {link}",
        "username": "Güvenlik Gözcüsü Bot",
        "avatar_url": "https://i.imgur.com/kG4j0kE.png" 
    }

    try:
        requests.post(webhook_url, json=payload)
        print(f"Discord'a başarıyla gönderildi: {link}")
    except Exception as e:
        print(f"Discord Webhook Hatası: {e}")

# --- BOTU ÇALIŞTIR ---
if __name__ == "__main__":
    live_link = get_live_stream_link(YOUTUBE_API_KEY, CHANNEL_ID)
    send_discord_notification(DISCORD_WEBHOOK_URL, live_link)
