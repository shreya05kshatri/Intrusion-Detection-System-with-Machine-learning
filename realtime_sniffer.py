from scapy.all import sniff
import requests
import json

# URL of your Flask API
API_URL = "http://127.0.0.1:8000/predict_api"

def extract_features(packet):
    try:
        # testing structure 
        features = {
            "duration": 0,
            "protocol_type": "tcp",
            "service": "http",
            "flag": "SF",
            "src_bytes": len(packet),
            "dst_bytes": 0,
            "count": 1
        }

        return features
    except Exception as e:
        print("Feature extraction error:", e)
        return None

def packet_callback(packet):
    features = extract_features(packet)
    if features:
        try:
            response = requests.post(API_URL, json=features)
            result = response.json()
            print(f"[+] Prediction: {result.get('prediction', 'Unknown')}")
        except Exception as e:
            print("Error sending packet for prediction:", e)

print("[*] Starting packet sniffing...")
sniff(prn=packet_callback, store=0)
