import tkinter as tk
from tkinter import messagebox
from tkinter import font
from nltk.corpus import words
from collections import deque



def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x[1] < pivot[1]]
    middle = [x for x in arr if x[1] == pivot[1]]
    right = [x for x in arr if x[1] > pivot[1]]
    return quicksort(left) + middle + quicksort(right)



class BSTNode:
    def __init__(self, word):
        self.word = word
        self.left = None
        self.right = None



class BST:
    def __init__(self):
        self.root = None

    def insert(self, word):
        if not self.root:
            self.root = BSTNode(word)
        else:
            self._insert(self.root, word)

    def _insert(self, node, word):
        if word < node.word:
            if node.left:
                self._insert(node.left, word)
            else:
                node.left = BSTNode(word)
        elif word > node.word:
            if node.right:
                self._insert(node.right, word)
            else:
                node.right = BSTNode(word)

    def search(self, word):
        return self._search(self.root, word)

    def _search(self, node, word):
        if not node:
            return False
        if node.word == word:
            return True
        elif word < node.word:
            return self._search(node.left, word)
        else:
            return self._search(node.right, word)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.word)
            self._inorder(node.right, result)


def levenshtein_distance(s1, s2):
    len_s1 = len(s1) + 1
    len_s2 = len(s2) + 1

    matrix = [[0] * len_s2 for _ in range(len_s1)]

    for i in range(len_s1):
        matrix[i][0] = i
    for j in range(len_s2):
        matrix[0][j] = j

    for i in range(1, len_s1):
        for j in range(1, len_s2):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,  
                matrix[i][j - 1] + 1,  
                matrix[i - 1][j - 1] + cost,  
            )

    return matrix[len_s1 - 1][len_s2 - 1]


class SpellCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSA Enhanced Spell Checker")
        self.root.geometry("400x500")
        self.root.configure(bg="#e6f7ff")

        
        self.bst = BST()
        self.word_list = set(words.words())  
        for word in self.word_list:
            self.bst.insert(word)

        self.create_widgets()

    def create_widgets(self):
        header_font = font.Font(family="Helvetica", size=16, weight="bold")

        self.header_label = tk.Label(
            self.root,
            text="Welcome to Spell Checker!",
            font=header_font,
            bg="#0099cc",
            fg="white",
        )
        self.header_label.pack(pady=10, fill=tk.X)

        self.word_label = tk.Label(
            self.root, text="Enter a word:", bg="#e6f7ff", fg="#003366", font=("Arial", 12)
        )
        self.word_label.pack(pady=5)

        self.word_entry = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 12),
            highlightbackground="#80d4ff",
            highlightthickness=2,
        )
        self.word_entry.pack(pady=5)

        self.check_button = tk.Button(
            self.root,
            text="Check Spelling",
            command=self.check_spelling,
            bg="#80d4ff",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        self.check_button.pack(pady=10)

        self.suggestion_label = tk.Label(
            self.root,
            text="Suggested words:",
            bg="#e6f7ff",
            fg="#003366",
            font=("Arial", 12),
        )
        self.suggestion_label.pack(pady=5)

        self.suggestion_listbox = tk.Listbox(
            self.root,
            height=6,
            width=30,
            font=("Arial", 12),
            bg="#f2f9fc",
            fg="#003366",
            highlightbackground="#80d4ff",
            highlightthickness=2,
        )
        self.suggestion_listbox.pack(pady=5)

        self.suggestion_count_label = tk.Label(
            self.root,
            text="",
            bg="#e6f7ff",
            fg="#003366",
            font=("Arial", 10, "italic"),
        )
        self.suggestion_count_label.pack(pady=5)

    def check_spelling(self):
        word_to_check = self.word_entry.get().strip().lower()

        if not word_to_check:
            messagebox.showwarning("Input Error", "Please enter a word.")
            return

        self.suggestion_listbox.delete(0, tk.END)

        suggestions = self.suggest_word(word_to_check)

        if self.bst.search(word_to_check):
            messagebox.showinfo(
                "Correct Spelling", f"'{word_to_check}' is correctly spelled."
            )
        else:
            messagebox.showwarning(
                "Misspelled Word", f"'{word_to_check}' is likely misspelled."
            )

            if suggestions:
                for suggestion in suggestions:
                    self.suggestion_listbox.insert(tk.END, suggestion)
                self.suggestion_count_label.config(
                    text=f"{len(suggestions)} suggestions found."
                )
            else:
                messagebox.showinfo("No Suggestions", "No suggestions found.")
                self.suggestion_count_label.config(text="0 suggestions found.")

    def suggest_word(self, word, threshold=2, max_suggestions=5):
        suggestions = []
        queue = deque(self.bst.inorder())  

        while queue:
            dict_word = queue.popleft()
            dist = levenshtein_distance(word, dict_word)
            if dist <= threshold:
                suggestions.append((dict_word, dist))

        sorted_suggestions = quicksort(suggestions)
        return [word for word, _ in sorted_suggestions[:max_suggestions]]


root = tk.Tk()
app = SpellCheckerApp(root)
root.mainloop()