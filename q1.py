import re

# Test data for demonstration
test_text = """
The products are 100% natural. 
We offer a 3-month subscription plan for $45.99.
Our headquarters are located at 12345 S. Main St., Springfield, IL 62704.
You can reach us at 800-555-1234.
The special offer ends on 12/31/2025.
The project's code is available on GitHub.
Our team includes a developer, a designer, and a project manager.
Check out the product details at: https://www.example.com/product-info.
Please send feedback to feedback@example.org.
"""

def test_regex_patterns():
    """Test all 6 regex patterns with sample data."""
    
    # 1. Dates in MM/DD/YYYY format
    date_pattern = r'\b(0?[1-9]|1[0-2])\/(0?[1-9]|[12][0-9]|3[01])\/\d{4}\b'
    print("1. DATES (MM/DD/YYYY):")
    date_matches = re.findall(date_pattern, test_text)
    for match in date_matches:
        print(f"    Found: {'/'.join(match)}")
    print()
    
    # 2. URLs (http/https)
    url_pattern = r'https?:\/\/[^\s]+'
    print("2. URLS:")
    url_matches = re.findall(url_pattern, test_text)
    for match in url_matches:
        print(f"    Found: {match}")
    print()
    
    # 3. Email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    print("3. EMAIL ADDRESSES:")
    email_matches = re.findall(email_pattern, test_text)
    for match in email_matches:
        print(f"    Found: {match}")
    print()
    
    # 4. Currency amounts (e.g., $45.99)
    currency_pattern = r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?'
    print("4. CURRENCY AMOUNTS:")
    currency_matches = re.findall(currency_pattern, test_text)
    for match in currency_matches:
        print(f"    Found: {match}")
    print()
    
    # 5. Words that are exactly 3 letters long
    three_letter_word_pattern = r'\b[A-Za-z]{3}\b'
    print("5. THREE-LETTER WORDS:")
    three_letter_matches = re.findall(three_letter_word_pattern, test_text)
    for match in three_letter_matches:
        print(f"    Found: {match}")
    print()
    
    # 6. Phone numbers (e.g., ###-###-####)
    phone_number_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    print("6. PHONE NUMBERS:")
    phone_number_matches = re.findall(phone_number_pattern, test_text)
    for match in phone_number_matches:
        print(f"    Found: {match}")
    print()

if __name__ == "__main__":
    # Run all examples
    test_regex_patterns()
    
    print("\n" + "="*60)
    print("SUMMARY OF PATTERNS:")
    print("="*60)
    patterns = {
        "Dates": r'\b(0?[1-9]|1[0-2])\/(0?[1-9]|[12][0-9]|3[01])\/\d{4}\b',
        "URLs": r'https?:\/\/[^\s]+',
        "Email addresses": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "Currency amounts": r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?',
        "3-letter words": r'\b[A-Za-z]{3}\b',
        "Phone numbers": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    }
    
    for name, pattern in patterns.items():
        print(f"{name:18}: {pattern}")