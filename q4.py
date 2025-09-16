import numpy as np

def edit_distance(s1, s2, sub_cost=1, ins_cost=1, del_cost=1):
    """Compute minimum edit distance with DP"""
    m, n = len(s1), len(s2)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    
    # Initialize first row and column
    for i in range(m + 1):
        dp[i][0] = i * del_cost
    for j in range(n + 1):
        dp[0][j] = j * ins_cost
    
    # Fill DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # Match
            else:
                substitute = dp[i-1][j-1] + sub_cost
                insert = dp[i][j-1] + ins_cost  
                delete = dp[i-1][j] + del_cost
                dp[i][j] = min(substitute, insert, delete)
    
    return dp[m][n], dp

def get_alignment(s1, s2, dp, sub_cost=1, ins_cost=1, del_cost=1):
    """Backtrack to get one valid edit sequence"""
    i, j = len(s1), len(s2)
    operations = []
    
    while i > 0 or j > 0:
        # Match/Substitute
        if i > 0 and j > 0 and s1[i-1] == s2[j-1] and dp[i][j] == dp[i-1][j-1]:
            operations.append(f"Match '{s1[i-1]}'")
            i, j = i-1, j-1
        # Substitute
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + sub_cost:
            operations.append(f"Substitute '{s1[i-1]}' -> '{s2[j-1]}'")
            i, j = i-1, j-1
        # Insert
        elif j > 0 and dp[i][j] == dp[i][j-1] + ins_cost:
            operations.append(f"Insert '{s2[j-1]}'")
            j = j-1
        # Delete
        elif i > 0 and dp[i][j] == dp[i-1][j] + del_cost:
            operations.append(f"Delete '{s1[i-1]}'")
            i = i-1
        else:
            # Fallback for paths with equal cost
            if i > 0 and j > 0:
                operations.append(f"Substitute '{s1[i-1]}' -> '{s2[j-1]}'")
                i, j = i-1, j-1
            elif j > 0:
                operations.append(f"Insert '{s2[j-1]}'")
                j = j-1
            elif i > 0:
                operations.append(f"Delete '{s1[i-1]}'")
                i = i-1
    
    return list(reversed(operations))

# Q4: New example: Kitten -> Sitting
print("Q4: Edit Distance - Kitten -> Sitting")
print("=" * 40)

s1, s2 = "Kitten", "Sitting"

# Model A: Sub=1, Ins=1, Del=1
print("\nModel A (Sub=1, Ins=1, Del=1):")
dist_a, matrix_a = edit_distance(s1, s2, 1, 1, 1)
alignment_a = get_alignment(s1, s2, matrix_a, 1, 1, 1)

print(f"Minimum edit distance: {dist_a}")
print("Edit sequence:")
for i, op in enumerate(alignment_a, 1):
    print(f"  {i}. {op}")

# Model B: Sub=2, Ins=1, Del=1  
print("\nModel B (Sub=2, Ins=1, Del=1):")
dist_b, matrix_b = edit_distance(s1, s2, 2, 1, 1)
alignment_b = get_alignment(s1, s2, matrix_b, 2, 1, 1)

print(f"Minimum edit distance: {dist_b}")
print("Edit sequence:")
for i, op in enumerate(alignment_b, 1):
    print(f"  {i}. {op}")

# Reflection
print("\nReflection:")
print("-" * 20)

same_distance = "Yes" if dist_a == dist_b else "No"
print(f"1. Did both models give the same distance? {same_distance} (A={dist_a}, B={dist_b})")

print("2. Which operations were most useful?")
print("   - For both models, the most useful operations were a combination of `Substitution` and `Insertion`. The transformation from 'K' to 'S' is a substitution, and the addition of 'g' at the end of 'Sitting' is an insertion. The core sequence 'itten' is a perfect match.")

print("3. How do the different models affect potential applications?")
print("   - **Spell Check:** In a spell checker, where typos are often single-character substitutions or insertions/deletions, Model A is a good choice because it gives equal weight to all operations. A user who types 'sitten' instead of 'sitting' would be easily corrected.")
print("   - **DNA Alignment:** For tasks like aligning DNA sequences, where insertions and deletions (indels) are common mutations, Model B would be more appropriate. By giving a higher cost to substitution, Model B encourages the algorithm to find an alignment path that uses indels over substitutions, which may better reflect a genetic process.")