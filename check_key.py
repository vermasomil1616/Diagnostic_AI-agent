from google import genai

# PASTE YOUR KEY HERE
MY_KEY = "AIzaSyBOZ2jdYdzSEgFSzbEYV3aQiAQAd99a3ts" 

try:
    client = genai.Client(api_key=MY_KEY)
    print("\n✅ SUCCESS! API Key is working.")
    print("Here are the models you can use:")

    # List all models available to you
    for m in client.models.list():
        if "generateContent" in m.supported_actions:
            # print only the clean name (e.g., gemini-1.5-flash)
            print(f" - {m.name.split('/')[-1]}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")

# AIzaSyBOZ2jdYdzSEgFSzbEYV3aQiAQAd99a3ts