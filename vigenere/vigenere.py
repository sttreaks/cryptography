from collections import Counter
import matplotlib.pyplot as plt


class Vigenere:
    def __init__(self, text, key="", language=""):
        self.language = language
        self.text = text.replace(" ", "").lower()
        self.key = key
        self.lang_len = len(language) - 1

    def encrypt(self):
        encrypted = ""
        key_letter = 0
        for letter in self.text:
            encrypted += self.language[(self.language.find(letter) + self.language.find(self.key[key_letter])) % self.lang_len]
            key_letter += 1
            if key_letter >= len(self.key):
                key_letter -= len(self.key)

        return encrypted

    def histogram(self):
        d = {}
        c = Counter(self.text)
        for letter in self.language:
            d.update({letter: c[letter]})
        print(d)
        plt.hist(list(d.keys()), list(d.values()))
        plt.show()

    def decrypt(self):
        decrypted = ""
        if self.key == "":
            for key_len in range(self.lang_len):
                pass
        else:
            key_letter = 0
            for letter in self.text:
                pos = self.language.find(letter) - self.language.find(self.key[key_letter])
                key_letter += 1
                if pos < 0:
                    pos = self.lang_len + pos
                if key_letter >= len(self.key):
                    key_letter -= len(self.key)
                decrypted += self.language[pos]

        return decrypted


if __name__ == '__main__':
    # print(Vigenere("веснакраснаколисьприйде", "зима", "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя").encrypt())
    # print(Vigenere("імднзфґаьчмкчхцсєщґитлт", "зима", "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя").decrypt())
    # print(Vigenere("ьччжпчьишисажакпявааьяч", "зима", "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя").decrypt())

    with open("books/shorada", "r") as f:
        text = f.read()

    Vigenere(text, language="абвгґдеєжзиіїйклмнопрстуфхцчшщьюя").histogram()
