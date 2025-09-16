import re
import nltk
import spacy
from nltk.tokenize import word_tokenize
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please install spaCy English model: python -m spacy download en_core_web_sm")
    nlp = None

# Sample paragraph from a science article about space exploration
paragraph = """The James Webb Space Telescope's stunning images weren't just for show; they've provided a new understanding of our universe. Astronomers couldn't have predicted the strange-looking galaxies they'd find. Its findings are truly mind-boggling."""

print("ORIGINAL PARAGRAPH:")
print("-" * 50)
print(paragraph)
print("\n")

def naive_tokenization(text):
    """Simple space-based tokenization"""
    return text.split()

def manual_tokenization(text):
    """Manual tokenization handling punctuation, contractions, and special cases"""
    tokens = []
    
    # First, handle contractions and special cases
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "can not", text)  # or "cannot"
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"'re", " are", text)
    text = re.sub(r"'ve", " have", text)
    text = re.sub(r"'ll", " will", text)
    text = re.sub(r"'d", " would", text)  # or "had" - context dependent
    
    # Handle possessives
    text = re.sub(r"'s\b", " 's", text)
    
    # Split on whitespace
    words = text.split()
    
    for word in words:
        # Handle punctuation at the end
        if re.search(r'[.!?,:;]$', word) and len(word) > 1:
            # Separate punctuation from word
            punct = word[-1]
            word_part = word[:-1]
            
            # Handle special cases like "U.S." or "Ph.D."
            if word_part.endswith('.') and len(word_part) <= 4:
                tokens.append(word)  # Keep abbreviations intact
            else:
                tokens.append(word_part)
                tokens.append(punct)
        else:
            tokens.append(word)
    
    return tokens

def highlight_differences(naive_tokens, manual_tokens):
    """Highlight differences between tokenization approaches"""
    print("DIFFERENCES ANALYSIS:")
    print("-" * 50)
    
    naive_set = set(naive_tokens)
    manual_set = set(manual_tokens)
    
    only_in_naive = naive_set - manual_set
    only_in_manual = manual_set - naive_set
    
    print(f"Tokens only in naive: {sorted(only_in_naive)}")
    print(f"Tokens only in manual: {sorted(only_in_manual)}")
    
    print(f"\nNaive token count: {len(naive_tokens)}")
    print(f"Manual token count: {len(manual_tokens)}")

def analyze_tokenization():
    """Main tokenization analysis"""
    
    # 1. Naive tokenization
    print("1. NAIVE SPACE-BASED TOKENIZATION:")
    print("-" * 50)
    naive_tokens = naive_tokenization(paragraph)
    for i, token in enumerate(naive_tokens, 1):
        print(f"{i:2d}. '{token}'")
    
    print(f"\nTotal tokens: {len(naive_tokens)}\n")
    
    # 2. Manual tokenization
    print("2. MANUAL TOKENIZATION (corrected):")
    print("-" * 50)
    manual_tokens = manual_tokenization(paragraph)
    for i, token in enumerate(manual_tokens, 1):
        print(f"{i:2d}. '{token}'")
    
    print(f"\nTotal tokens: {len(manual_tokens)}\n")
    
    # Highlight differences
    highlight_differences(naive_tokens, manual_tokens)
    
    return naive_tokens, manual_tokens

def compare_with_tools(manual_tokens):
    """Compare manual tokenization with NLP tools"""
    
    print("\n3. COMPARISON WITH NLP TOOLS:")
    print("-" * 50)
    
    # NLTK tokenization with error handling
    print("NLTK Word Tokenizer:")
    try:
        nltk_tokens = word_tokenize(paragraph)
        for i, token in enumerate(nltk_tokens, 1):
            print(f"{i:2d}. '{token}'")
        print(f"Total tokens: {len(nltk_tokens)}")
    except Exception as e:
        print(f"NLTK tokenization failed: {e}")
        print("Using fallback regex-based tokenization...")
        # Fallback tokenization
        nltk_tokens = re.findall(r"\b\w+(?:'\w+)?\b|[^\w\s]", paragraph)
        for i, token in enumerate(nltk_tokens, 1):
            print(f"{i:2d}. '{token}' (fallback)")
        print(f"Total tokens: {len(nltk_tokens)} (fallback)")
    
    # spaCy tokenization
    if nlp:
        print("\nspaCy Tokenizer:")
        doc = nlp(paragraph)
        spacy_tokens = [token.text for token in doc]
        for i, token in enumerate(spacy_tokens, 1):
            print(f"{i:2d}. '{token}'")
        print(f"Total tokens: {len(spacy_tokens)}")
    else:
        spacy_tokens = []
    
    # Compare differences
    print("\nDIFFERENCES WITH TOOLS:")
    print("-" * 30)
    
    manual_set = set(manual_tokens)
    nltk_set = set(nltk_tokens)
    
    print("Manual vs NLTK:")
    print(f"  Only in manual: {sorted(manual_set - nltk_set)}")
    print(f"  Only in NLTK: {sorted(nltk_set - manual_set)}")
    
    if spacy_tokens:
        spacy_set = set(spacy_tokens)
        print("\nManual vs spaCy:")
        print(f"  Only in manual: {sorted(manual_set - spacy_set)}")
        print(f"  Only in spaCy: {sorted(spacy_set - manual_set)}")
    
    return nltk_tokens, spacy_tokens

def identify_multiword_expressions():
    """Identify and analyze multiword expressions"""
    
    print("\n4. MULTIWORD EXPRESSIONS (MWEs):")
    print("-" * 50)
    
    # MWEs found in our paragraph
    mwes = [
        {
            "expression": "James Webb Space Telescope",
            "type": "Proper Noun/Technical Term",
            "reason": "This is a specific, named entity that refers to a single object. It should not be broken apart.",
            "tokens": ["James", "Webb", "Space", "Telescope"]
        },
        {
            "expression": "mind-boggling",
            "type": "Compound adjective",
            "reason": "Hyphenated compound that functions as a single adjective meaning 'extremely surprising'",
            "tokens": ["mind-boggling"]
        },
        {
            "expression": "for show",
            "type": "Idiomatic phrase",
            "reason": "An idiom where the meaning is not the sum of its parts; it means 'for appearance's sake'.",
            "tokens": ["for", "show"]
        },
        {
            "expression": "our universe",
            "type": "Technical term/Collocation",
            "reason": "A phrase that represents a specific concept in a scientific context and is often treated as a single unit.",
            "tokens": ["our", "universe"]
        },
        {
            "expression": "strange-looking",
            "type": "Compound adjective",
            "reason": "Another hyphenated compound that functions as a single descriptor for 'galaxies'",
            "tokens": ["strange-looking"]
        }
    ]
    
    for i, mwe in enumerate(mwes, 1):
        print(f"{i}. '{mwe['expression']}'")
        print(f"  Type: {mwe['type']}")
        print(f"  Reason: {mwe['reason']}")
        print(f"  Would be tokenized as: {mwe['tokens']}")
        print()

def advanced_analysis():
    """Additional analysis of tokenization challenges"""
    
    print("5. ADVANCED TOKENIZATION CHALLENGES:")
    print("-" * 50)
    
    challenges = {
        "Contractions": {
            "examples": ["weren't", "they've", "couldn't"],
            "issue": "Deciding whether to split into two words (e.g., were not) or keep as a single token.",
            "solution": "NLP tools typically split them for consistent part-of-speech tagging and analysis."
        },
        "Hyphenated words": {
            "examples": ["strange-looking", "mind-boggling"],
            "issue": "These words should ideally be kept as single tokens to preserve their semantic meaning.",
            "solution": "Robust tokenizers recognize the compound nature and keep them intact."
        },
        "Possessives": {
            "examples": ["Telescope's", "they'd"],
            "issue": "The 's can be a possessive ('Telescope's') or a contraction ('they'd').",
            "solution": "Tools like spaCy use a statistical model to disambiguate the 's and tokenize accordingly."
        },
        "Punctuation": {
            "examples": [",", ";"],
            "issue": "Punctuation needs to be separated from words as its own token for syntactic analysis.",
            "solution": "Most professional tokenizers like NLTK and spaCy handle this by default."
        }
    }
    
    for challenge, details in challenges.items():
        print(f"{challenge}:")
        print(f"  Examples: {', '.join(details['examples'])}")
        print(f"  Issue: {details['issue']}")
        print(f"  Solution: {details['solution']}")
        print()

def reflection():
    """Reflection on tokenization challenges"""
    
    print("6. REFLECTION:")
    print("-" * 50)
    
    reflection_text = """
    The hardest part of tokenization in English is handling ambiguities, such as contractions and hyphenated compounds. My manual tokenizer struggled with contractions like "they've" and "couldn't" because a simple regex isn't always context-aware, while professional tools like NLTK and spaCy correctly identified these as single-token units or split them correctly. This highlights a key difference between rule-based and statistical tokenizers.
    
    Compared to some other languages, English tokenization is relatively simple due to its use of spaces. However, it still has challenges with punctuation, proper nouns, and multiword expressions. The tools handled these cases by leveraging trained models that understand grammatical structures, which is a significant advantage over my manual, rule-based approach. The importance of robust tokenization lies in its impact on all subsequent NLP tasks, as errors introduced here can propagate and affect a model's performance.
    """
    
    print(reflection_text.strip())

if __name__ == "__main__":
    # Run complete analysis
    naive_tokens, manual_tokens = analyze_tokenization()
    nltk_tokens, spacy_tokens = compare_with_tools(manual_tokens)
    identify_multiword_expressions()
    advanced_analysis()
    reflection()
    
    # Summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS:")
    print("="*60)
    print(f"Naive tokenization:   {len(naive_tokens):2d} tokens")
    print(f"Manual tokenization:  {len(manual_tokens):2d} tokens")
    print(f"NLTK tokenization:    {len(nltk_tokens):2d} tokens")
    if spacy_tokens:
        print(f"spaCy tokenization:   {len(spacy_tokens):2d} tokens")