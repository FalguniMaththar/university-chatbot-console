import re
from difflib import SequenceMatcher

STOPWORDS = {
    'a','an','the','is','are','was','were','in','on','at','for','of','and','or','to','how','what','when','which','my','i'
}

def preprocess(text: str):
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    tokens = [t for t in s.split() if t and t not in STOPWORDS]
    return ' '.join(tokens), tokens

def jaccard(a_tokens, b_tokens):
    sa, sb = set(a_tokens), set(b_tokens)
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

def similarity(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio()

def best_match(user_text: str, faqs: list, threshold=0.45):
    pre_user, user_tokens = preprocess(user_text)
    best = None
    best_score = 0.0
    for f in faqs:
        q = f.get('question', '')
        pre_q, q_tokens = preprocess(q)
        seq = similarity(pre_user, pre_q)
        jac = jaccard(user_tokens, q_tokens)
        score = 0.7 * seq + 0.3 * jac
        if score > best_score:
            best_score = score
            best = f
    if best_score >= threshold:
        return best, best_score
    return None, best_score