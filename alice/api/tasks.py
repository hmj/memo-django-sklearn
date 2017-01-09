from django.core.cache import cache

from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups

from .models import CountVectorizerParameter, TopicModelParamter
from .predictor import Predictor

from celery import shared_task


def get_topicwords_key(name):
    return "topicwords:{0}".format(name)

def save_models():
    dataset = fetch_20newsgroups(shuffle=True, random_state=1,
                                 remove=('headers', 'footers', 'quotes'))
    data_samples = dataset.data[:2000]

    params = CountVectorizerParameter.get_params()
    print(params)
    tf_vectorizer = CountVectorizer(**params)
    tf_vectorizer.fit(data_samples)
    tf = tf_vectorizer.fit_transform(data_samples)
    joblib.dump(tf_vectorizer, 'tf_vectorizer.pkl')

    params = TopicModelParamter.get_params()
    print(params)
    lda = LatentDirichletAllocation(**params)
    lda.fit(tf)
    joblib.dump(lda, 'lda.pkl')


def upload_predictor():
    """
    cacheにpredictorをセットする

    :return:
    """
    clf = Predictor()
    clf.load()
    cache.set('__predictor', clf, 3600)
