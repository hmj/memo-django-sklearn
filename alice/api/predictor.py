from django.utils import timezone

from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

from celery import task, Task


class Predictor:
    def __init__(self):
        self.created = timezone.datetime.now()

    def load(self):
        self.nanika1 = joblib.load('tf_vectorizer.pkl')
        self.nanika2 = joblib.load('lda.pkl')
        self.lda = Pipeline([
            ('vect', self.nanika1),
            ('clf', self.nanika2)
        ])

    def predict(self, name):
        return self.lda.transform([name])


    def analyze(self, name):
        _a = self.nanika1.build_analyzer()
        res = _a(name)
        return res

    __call__ = predict

print('default_predict')
default_predict = Predictor()

@task
def add(x, y):
    return default_predict.load()

