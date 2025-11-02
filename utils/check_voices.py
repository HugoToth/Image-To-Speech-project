import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("--- Available Voices ---")
for index, voice in enumerate(voices):
    print(f"\nVoice {index}:")
    print(f"  ID: {voice.id}")
    print(f"  Name: {voice.name}")
    print(f"  Language: {voice.languages}")
    print(f"  Gender: {voice.gender}")
    print(f"  Age: {voice.age}")
print("\n-------------------------")