import json

import ananas
import markovify

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

class Shakey(ananas.PineappleBot):
    def start(self):
        with open('shakespeare.json') as f:
            text = json.load(f)
        self.text_model = POSifiedText.from_json(text)

    @ananas.hourly(minute=11)
    def post_markov_sentence(self):
        self.mastodon.toot(self.text_model.make_sentence())
