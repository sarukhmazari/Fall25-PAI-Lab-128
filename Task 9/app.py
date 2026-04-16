from textblob import TextBlob


text = input("Enter a sentence for analysis: ")

blob = TextBlob(text)

polarity = blob.sentiment.polarity
subjectivity = blob.sentiment.subjectivity

print("\nProcessing text...\n")

print("Original Text:")
print(text)

print("\nAnalysis Results:")
print("Polarity Score:", polarity)
print("Subjectivity Score:", subjectivity)

if polarity > 0:
    print("\nSentiment: Positive")
elif polarity < 0:
    print("\nSentiment: Negative")
else:
    print("\nSentiment: Neutral")

