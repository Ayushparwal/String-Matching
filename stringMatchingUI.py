import tkinter as tk
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Abbreviations for preprocessing
abbreviations = {
    "st": "street", 
    "rd": "road", 
    "ave": "avenue", 
    "blvd": "boulevard", 
    "dr": "drive", 
    "ln": "lane",
    "hwy": "highway",
    "rt": "route",
    "pkwy": "parkway",
    "ct": "court",
    "s": "south",
    "e": "east",
    "w": "west",
    "n": "north"
}

# Preprocessing function for the address
def preprocess_address(address, abbreviations):
    address = address.lower()
    for abbr, full in abbreviations.items():
        address = re.sub(r'\b' + re.escape(abbr) + r'\b', full, address)
    address = re.sub(r'\s+', ' ', address).strip()
    return address

# Function to extract features
def extract_features(addr1, addr2):
    addr1 = preprocess_address(addr1, abbreviations)
    addr2 = preprocess_address(addr2, abbreviations)
    
    fuzzy_score = fuzz.ratio(addr1, addr2) / 100
    
    vectorizer = TfidfVectorizer().fit_transform([addr1, addr2])
    cosine_score = cosine_similarity(vectorizer)[0, 1]
    
    set1, set2 = set(addr1.split()), set(addr2.split())
    jaccard_score = len(set1 & set2) / len(set1 | set2)
    
    zip_match = 1 if addr1.split()[-1] == addr2.split()[-1] else 0
    
    return [fuzzy_score, cosine_score, jaccard_score, zip_match]

def calculate_scores():
    address1 = entry_address1.get()  # Get the first address
    address2 = entry_address2.get()  # Get the second address
    
    scores = extract_features(address1, address2)
    
    label_fuzzy_score.config(text=f"Fuzzy Match Score: {scores[0]:.2f}")
    label_cosine_score.config(text=f"Cosine Similarity: {scores[1]:.2f}")
    label_jaccard_score.config(text=f"Jaccard Similarity: {scores[2]:.2f}")
    label_zip_match.config(text=f"Zip Match: {scores[3]}")


root = tk.Tk()
root.title("Address Similarity Scorer")

# Set window size
root.geometry("900x500")

# Add a label for the first address
label_address1 = tk.Label(root, text="Enter Address 1:")
label_address1.pack(pady=5)

# Add an entry widget for Address 1
entry_address1 = tk.Entry(root, width=50)
entry_address1.pack(pady=5)

# Add a label for the second address
label_address2 = tk.Label(root, text="Enter Address 2:")
label_address2.pack(pady=5)

# Add an entry widget for Address 2
entry_address2 = tk.Entry(root, width=50)
entry_address2.pack(pady=5)

# Add a button to calculate the scores
button_calculate = tk.Button(root, text="Calculate Scores", command=calculate_scores)
button_calculate.pack(pady=10)

# Add labels to display the results
label_fuzzy_score = tk.Label(root, text="Fuzzy Match Score: ", font=("Arial", 12))
label_fuzzy_score.pack(pady=5)

label_cosine_score = tk.Label(root, text="Cosine Similarity: ", font=("Arial", 12))
label_cosine_score.pack(pady=5)

label_jaccard_score = tk.Label(root, text="Jaccard Similarity: ", font=("Arial", 12))
label_jaccard_score.pack(pady=5)

label_zip_match = tk.Label(root, text="Zip Match: ", font=("Arial", 12))
label_zip_match.pack(pady=5)

# Run the main event loop
root.mainloop()
