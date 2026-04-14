from model import predict_label

# test inputs
test_cases = [
    "Python tutorial",
    "SQL course",
    "Funny reels",
    "Gaming video",
    "Machine learning lecture",
    "Free fire gameplay",
    "GitHub repository",
    "Watching movie trailer"
]

# run tests
for text in test_cases:
    result = predict_label(text)
    print(f"{text} --> {result}")