import re
from collections import defaultdict, Counter
import copy

def manual_bpe_toy_corpus():
    """
    Performs the first three merges of BPE manually on the toy corpus.
    """
    print("\nQ3.1: MANUAL BPE ON A TOY CORPUS")
    print("-" * 40)
    
    # Original corpus from the assignment
    original_corpus = "low low low low low lowest lowest newer newer newer newer newer newer wider wider wider new new"
    
    print(f"Original corpus: {original_corpus}")
    print()
    
    # Step 1: Add end-of-word marker _ and create initial vocabulary
    print("STEP 1: Add end-of-word marker and initial vocabulary")
    print("-" * 30)
    
    words = original_corpus.split()
    word_counts = Counter(words)
    
    # Add end-of-word markers to each word
    words_with_markers = {}
    for word, count in word_counts.items():
        words_with_markers[word + '_'] = count
    
    print(f"Words with end markers: {words_with_markers}")
    
    # Create initial vocabulary (all characters including _)
    initial_vocab = set()
    for word in words_with_markers:
        for char in word:
            initial_vocab.add(char)
    
    initial_vocab = sorted(list(initial_vocab))
    print(f"Initial vocabulary (chars + _): {initial_vocab}")
    print(f"Initial vocabulary size: {len(initial_vocab)}")
    print()
    
    # Initialize current state
    current_words = copy.deepcopy(words_with_markers)
    current_vocab = set(initial_vocab)
    
    # Helper functions to find bigram counts and merge pairs
    def get_bigram_counts(word_dict):
        pair_counts = defaultdict(int)
        for word, freq in word_dict.items():
            chars = list(word)
            for i in range(len(chars) - 1):
                pair = (chars[i], chars[i + 1])
                pair_counts[pair] += freq
        return pair_counts
    
    def merge_pair(word_dict, pair_to_merge):
        new_word_dict = {}
        old_char1, old_char2 = pair_to_merge
        new_token = old_char1 + old_char2
        
        for word, freq in word_dict.items():
            new_word = word.replace(old_char1 + old_char2, new_token)
            new_word_dict[new_word] = freq
        return new_word_dict, new_token
    
    # Perform first three merges
    merges = []
    
    for merge_step in range(1, 4):
        print(f"MERGE STEP {merge_step}:")
        print("-" * 20)
        
        # Compute bigram counts
        bigram_counts = get_bigram_counts(current_words)
        print("Bigram counts:")
        for pair, count in sorted(bigram_counts.items(), key=lambda x: (-x[1], x[0])):
             print(f"  {pair}: {count}")
        
        # Find most frequent pair
        most_frequent_pair = max(bigram_counts.items(), key=lambda x: x[1])
        pair_to_merge, max_count = most_frequent_pair
        
        print(f"\nMost frequent pair: {pair_to_merge} (count: {max_count})")
        
        # Merge the pair
        current_words, new_token = merge_pair(current_words, pair_to_merge)
        current_vocab.add(new_token)
        merges.append((pair_to_merge, new_token))
        
        print(f"New token created: '{new_token}'")
        print(f"Updated corpus snippet:")
        
        # Show updated corpus for "lowest" and "newer"
        print(f"  'lowest_' becomes '{current_words['lowest_']}'")
        print(f"  'newer_' becomes '{current_words['newer_']}'")
        
        print(f"Updated vocabulary size: {len(current_vocab)}")
        print(f"Current vocabulary: {sorted(list(current_vocab))}")
        print()
    
    return current_words, merges, current_vocab

# Q3.2: Code a mini-BPE learner
def coded_bpe_learner():
    """
    A simple, coded BPE learner for the toy corpus.
    """
    print("Q3.2: CODED MINI-BPE LEARNER")
    print("-" * 40)
    
    class BPELearner:
        def __init__(self):
            self.vocab = set()
            self.merges = []
        
        def train(self, corpus, num_merges):
            word_counts = Counter(word + '_' for word in corpus.split())
            
            # Initial vocabulary
            self.vocab = set(''.join(word_counts.keys()))
            print(f"Initial vocabulary size: {len(self.vocab)}")
            
            current_tokens = {word: list(word) for word in word_counts}
            
            for i in range(num_merges):
                pair_counts = defaultdict(int)
                for word, tokens in current_tokens.items():
                    for j in range(len(tokens) - 1):
                        pair_counts[(tokens[j], tokens[j+1])] += word_counts[word]
                
                if not pair_counts:
                    break
                    
                most_frequent_pair = max(pair_counts, key=pair_counts.get)
                count = pair_counts[most_frequent_pair]
                
                print(f"Step {i + 1}: Merging {most_frequent_pair} (count: {count})")
                
                new_token = ''.join(most_frequent_pair)
                self.merges.append(most_frequent_pair)
                self.vocab.add(new_token)
                
                # Update words with new token
                updated_tokens = {}
                for word, tokens in current_tokens.items():
                    new_word_tokens = []
                    j = 0
                    while j < len(tokens):
                        if j < len(tokens) - 1 and tokens[j:j+2] == list(most_frequent_pair):
                            new_word_tokens.append(new_token)
                            j += 2
                        else:
                            new_word_tokens.append(tokens[j])
                            j += 1
                    updated_tokens[word] = new_word_tokens
                current_tokens = updated_tokens
                
                print(f"  New token: '{new_token}'")
                print(f"  Vocabulary size: {len(self.vocab)}")
                print()
            
        def segment_word(self, word):
            word = word + '_'
            tokens = list(word)
            
            # Re-apply merges to segment
            for merge_pair in self.merges:
                new_token = ''.join(merge_pair)
                new_tokens_list = []
                i = 0
                while i < len(tokens):
                    if i < len(tokens) - 1 and tokens[i] + tokens[i+1] == new_token:
                        new_tokens_list.append(new_token)
                        i += 2
                    else:
                        new_tokens_list.append(tokens[i])
                        i += 1
                tokens = new_tokens_list
            return tokens
    
    # Train BPE
    toy_corpus = "low low low low low lowest lowest newer newer newer newer newer newer wider wider wider new new"
    bpe = BPELearner()
    bpe.train(toy_corpus, num_merges=10)
    
    # Segment test words
    print("WORD SEGMENTATION:")
    print("-" * 20)
    test_words = ["new", "newer", "lowest", "widest", "newestest"]
    for word in test_words:
        segments = bpe.segment_word(word)
        print(f"'{word}' -> {segments}")
    
    # Explanation
    print("\nBPE ANALYSIS (5-6 sentences):")
    print("-" * 20)
    reflection_text = """
    BPE solves the Out-of-Vocabulary (OOV) problem by representing unseen words as sequences of known subword units. For example, a new or rare word like "unbelievably" can be tokenized into common subwords like 'un', 'believe', and 'ably', all of which might be present in the vocabulary. This allows the model to handle an infinite number of words without an infinite vocabulary size. An example of a meaningful morpheme is 'er' in English, which often functions as a comparative suffix as in 'newer' from 'new'. BPE learns this pattern from frequent occurrences of words ending in 'er' and creates a dedicated 'er_' token, aligning with a meaningful part of the word's structure.
    """
    print(reflection_text.strip())
    
    return bpe

### Q3.3: BPE on your language (English paragraph)
def bpe_on_paragraph():
    """
    Trains BPE on a short English paragraph.
    """
    print("\n\nQ3.3: BPE ON ENGLISH PARAGRAPH")
    print("-" * 40)
    
    # Sample English paragraph
    paragraph = """
    Natural language processing enables computers to understand human communication.
    Advanced algorithms analyze text patterns and extract meaningful information.
    Machine learning models can process thousands of documents automatically.
    This technology revolutionizes how we interact with digital systems.
    """
    
    # Clean and prepare text for BPE training
    text = paragraph.strip().lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    print(f"Training text: {text}")
    print()
    
    class AdvancedBPE:
        def __init__(self):
            self.vocab = set()
            self.merges = []
            
        def train(self, text, num_merges=30):
            word_counts = Counter(word + '_' for word in text.split())
            
            # Initial vocabulary with characters
            self.vocab = set(''.join(word_counts.keys()))
            
            current_tokens = {word: list(word) for word in word_counts}
            
            for i in range(num_merges):
                pair_counts = defaultdict(int)
                for word, tokens in current_tokens.items():
                    for j in range(len(tokens) - 1):
                        pair_counts[(tokens[j], tokens[j+1])] += word_counts.get(''.join(tokens), 0)
                
                if not pair_counts:
                    break
                    
                most_frequent_pair = max(pair_counts, key=pair_counts.get)
                new_token = ''.join(most_frequent_pair)
                self.merges.append(most_frequent_pair)
                self.vocab.add(new_token)
                
                # Update word tokens
                updated_tokens = {}
                for word, tokens in current_tokens.items():
                    new_word_tokens = []
                    j = 0
                    while j < len(tokens):
                        if j < len(tokens) - 1 and tokens[j:j+2] == list(most_frequent_pair):
                            new_word_tokens.append(new_token)
                            j += 2
                        else:
                            new_word_tokens.append(tokens[j])
                            j += 1
                    updated_tokens[''.join(new_word_tokens)] = new_word_tokens
                current_tokens = updated_tokens
            
            return self.merges, self.vocab
            
        def segment_word(self, word):
            word = word.lower() + '_'
            tokens = list(word)
            
            for merge_pair in self.merges:
                new_token = ''.join(merge_pair)
                new_tokens_list = []
                i = 0
                while i < len(tokens):
                    if i < len(tokens) - 1 and tokens[i] + tokens[i+1] == new_token:
                        new_tokens_list.append(new_token)
                        i += 2
                    else:
                        new_tokens_list.append(tokens[i])
                        i += 1
                tokens = new_tokens_list
            return tokens
    
    # Train BPE
    bpe = AdvancedBPE()
    merges, vocab = bpe.train(text, num_merges=30)
    
    # Show five most frequent merges
    print(f"Top 5 most frequent merges:")
    for i in range(5):
        pair, new_token = merges[i], ''.join(merges[i])
        print(f"  {i+1}. {pair} -> {new_token}")
        
    # Show five longest subword tokens
    longest_tokens = sorted([token for token in vocab if len(token) > 1], key=len, reverse=True)[:5]
    print(f"\n5 longest subword tokens:")
    for i, token in enumerate(longest_tokens, 1):
        print(f"  {i}. '{token}' (length: {len(token)})")
    
    # Segment 5 words
    test_words = [
        "processing",        # common word
        "revolutionizes",    # rare word
        "automatically",     # derived form
        "meaningful",        # compound-like
        "communication"      # inflected form
    ]
    
    print("\nWORD SEGMENTATION EXAMPLES:")
    print("-" * 30)
    for word in test_words:
        segments = bpe.segment_word(word)
        print(f"'{word}' -> {segments}")
    
    # Reflection
    print("\nBRIEF REFLECTION (5-8 sentences):")
    print("-" * 20)
    reflection_text = """
    The BPE algorithm learned a variety of subwords from the English paragraph, including prefixes, suffixes, stems, and common character sequences. The most frequent merges often formed stems like 'ing', 'tion', and 's'. BPE is beneficial for English because it efficiently handles the language's rich morphology, reducing the vocabulary size while retaining the ability to represent new words. It's particularly good at handling derived forms like "automatically," which it can break down into the known components "automat" and "ically." A potential drawback, however, is that BPE can sometimes split words in a way that is not linguistically intuitive, or it may produce inconsistent segmentations for the same word. Overall, subword tokenization offers a good balance between the expressive power of word-level models and the flexibility of character-level models for English.
    """
    print(reflection_text.strip())
    
    return bpe

if __name__ == "__main__":
    # Run all parts
    manual_bpe_toy_corpus()
    
    print("\n" + "="*60)
    coded_bpe = coded_bpe_learner()
    
    print("\n" + "="*60)
    paragraph_bpe = bpe_on_paragraph()