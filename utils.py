def api_call(text, ai):
    return "", ""



def extract_vote(text, names):
    for name in names:
        if name in text:
            return name
    return f"Error, no vote was recorded"