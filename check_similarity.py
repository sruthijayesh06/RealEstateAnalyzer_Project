from difflib import SequenceMatcher

test_words = [
    ("thiruvananthapuram", "trivandrum"),
    ("thiruvanantapuram", "trivandrum"),
    ("bangalore", "bangalore"),
    ("bengaluru", "bangalore"),
]

for word, city in test_words:
    score = SequenceMatcher(None, word, city).ratio()
    print(f"{word:30} vs {city:20} = {score:.3f}")
