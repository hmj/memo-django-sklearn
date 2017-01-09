from django.utils import timezone

from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

from celery import task, Task


class Predictor:
    def __init__(self):
        self.created = timezone.datetime.now()

    def analyze(self, name):
        lst = self.vectorizer.build_analyzer()(name)
        lst.sort()
        return ' '.join(lst)

    def load(self):
        self.vectorizer = joblib.load('tf_vectorizer.pkl')
        self.lda = Pipeline([
            ('vect', self.vectorizer),
            ('clf', joblib.load('lda.pkl'))
        ])
        self.loaded = True

    def predict(self, name):
        return self.lda.transform([name])

    __call__ = predict
