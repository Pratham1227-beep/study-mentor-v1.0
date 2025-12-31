def tips(text):
    words = list(set(text.split()))[:5]
    return f"Focus on: {', '.join(words)}"
