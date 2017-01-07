from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups

def save_models():
    dataset = fetch_20newsgroups(shuffle=True, random_state=1,
                                 remove=('headers', 'footers', 'quotes'))
    data_samples = dataset.data[:2000]

    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=2000, stop_words='english')
    tf_vectorizer.fit(data_samples)
    tf = tf_vectorizer.fit_transform(data_samples)
    joblib.dump(tf_vectorizer, 'tf_vectorizer.pkl')

    lda = LatentDirichletAllocation(n_topics=10, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)
    joblib.dump(lda, 'lda.pkl')

