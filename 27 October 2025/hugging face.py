from transformers import pipeline

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Input text
text = "I just bought a new electric car and it's incredibly efficient."

# Candidate labels
labels = ["technology", "environment", "automobile", "finance", "sports"]

# Run classification
result = classifier(text, candidate_labels=labels)

# Display results
print(f"Text: {text}")
print("Predicted labels and scores:")
for label, score in zip(result['labels'], result['scores']):
    print(f"{label}: {score:.2f}")
