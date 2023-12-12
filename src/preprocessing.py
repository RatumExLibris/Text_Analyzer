import re
import nltk
from pymorphy3 import MorphAnalyzer
from nltk.corpus import stopwords
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

class Pipeline:
    def __init__(self):
        with open('model/tags_names.txt', encoding='utf8') as f:
            self.tags_names = f.read().split(',')
        self.patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
        self.stopwords_ru = stopwords.words("russian")
        self.morph = MorphAnalyzer()
        self.model = pickle.load(open("model/model.pkl", "rb"))
        self.tags_embs = np.load('model/tags_embs.npy')
        self.tags = ''
        self.text = ''

    def _preprocess_text(self):
        self.text = re.sub(self.patterns, ' ', self.text)
        tokens = []
        for token in self.text.split():
            if token and token not in self.stopwords_ru:
                token = self.morph.normal_forms(token)[0]
                tokens.append(token)
        self.text = ' '.join(tokens)

    def _get_predictions(self):
        text_emb = self.model.transform([self.text])
        cosine_sim = np.array([cosine_similarity(tag_emb, text_emb)[0][0] for tag_emb in self.tags_embs])
        if cosine_sim.max() != 0:
            cosine_sim /= cosine_sim.max()
        self.tags = dict([(key, value) for i, (key, value) in enumerate(zip(self.tags_names, list(cosine_sim)))])

    def process(self):
        self._preprocess_text()
        self._get_predictions()

    def set_text(self, text):
        self.text = text

    def get_tags(self):
        return self.tags

pipeline = Pipeline()
text = 'В первобытном обществе уровень экономического развития был низким, обеспечивающим потребление на грани физического выживания. Сначала первобытные люди добывали средства к существованию охотой и собирательством, но в результате неолитической революции возникли земледелие и животноводство. Развитие общества привело к разделению труда — выделились земледельческие и пастушеские племена, выделились ремесленники, первыми из которых были кузнецы. Появились социальное неравенство, социальные классы и государство. Возникло рабовладение.\nПостепенно развивался товарообмен, который сначала осуществлялся в форме натурального обмена (бартера), но с появлением денег превратился в торговлю. Тем не менее, в обществах Древнего мира и Средневековья преобладающим было натуральное хозяйство. Во многих государствах древности существовала так называемая дворцовая экономика, основанная на сочетании планового хозяйства (позволяющего осуществлять крупные общественные работы, такие как орошение, сооружение дворцов и пирамид) и натурального хозяйства.'
pipeline.set_text(text)
pipeline.process()
print(pipeline.get_tags())