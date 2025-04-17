from collections import defaultdict, Counter
import math
import string
import re
import numpy as np

class NaiveBayesClassifier:

    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.classes = set()
        self.vocab = set()
        self.word_probs = defaultdict(lambda: defaultdict(float)) 
        self.class_probs = {}


    def clean_text(self, text):
        """Очистка текста от пунктуации и приведение к нижнему регистру"""
        translator = str.maketrans("", "", string.punctuation)
        return text.translate(translator).lower()
    
    
    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.classes = set(y)
        
    
        class_counts = Counter(y)
        total_docs = len(y)
        
        self.class_probs = {cls: math.log(count / total_docs) for cls, count in class_counts.items()}
        
        word_counts = defaultdict(lambda: defaultdict(int))
        class_word_totals = defaultdict(int)
        vocabulary = set()
        
        for text, cls in zip(X, y):
            words = self.clean_text(text).split()
            for word in words:
                word_counts[cls][word] += 1
                class_word_totals[cls] += 1
                vocabulary.add(word)
        
        self.vocab = vocabulary
        
        for cls in self.classes:
            total_words_in_class = class_word_totals[cls]
            for word in vocabulary:
                count = word_counts[cls][word]
                self.word_probs[cls][word] = math.log((count + self.alpha) / (total_words_in_class + self.alpha * len(vocabulary)))




    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predictions = []
        for text in X:
            words = self.clean_text(text).split()
            
            class_scores = {cls: self.class_probs[cls] for cls in self.classes}
            
            for word in words:
                for cls in self.classes:
                    if word in self.vocab:
                        class_scores[cls] += self.word_probs[cls].get(word, 0)
                    else:
                        class_scores[cls] += math.log(self.alpha / (len(self.vocab) + self.alpha))
            
            predicted_class = max(class_scores, key=class_scores.get)
            predictions.append(predicted_class)
        
        return predictions



    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predictions = self.predict(X_test)
        correct = sum(p == y for p, y in zip(predictions, y_test))
        return correct / len(y_test) if y_test else 0
