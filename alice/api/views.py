import time

from collections import OrderedDict

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .tasks import save_models, upload_predictor, get_topicwords_key


def return_ms(sec):
    return "{:.4f} ms".format(sec * 10**3)


class AnalysisView(APIView):
    def get(self, request, format=None):
        t1 = time.clock()
        raw_document = request.GET.get('name', None)

        """
        1. predictor cache get, ~10ms
        2. predictor.analyzer, raw_documentに前処理をかけて余分な単語を落とす, ~0.1ms
            --> tokens
        3. tokens が cache hit するか ~0.1ms
            y --> cacheの値を返す（topicのwordsのあつまりで，list）
            n --> 4.
        4. predictor(tokens)
            --> ldaにてtransformの計算をする
            --> 計算結果をcacheに格納する
            --> cacheの値を返す
        """
        try:
            t2 = time.clock()
            predictor = cache.get('__predictor')
            t3, time_cache_get = time.clock(), time.clock() - t2
            if not predictor:
                raise ValueError('predictor is not cache.')
            analyzed_document = predictor.analyze(raw_document)

            cache_key = get_topicwords_key(analyzed_document)
            cached = cache.get(cache_key)
            if cached is not None:
                res1 = 'cache hit: %s'.format(analyzed_document)
                data = cached
            else:
                res1 = 'cache no hit: %s'.format(analyzed_document)
                result_lda = predictor(analyzed_document)[0].max()
                # TODO 処理
                cache.set(cache_key, result_lda)
                data = cache.get(cache_key)
        except AttributeError as e:
            print(e)
            tokens = 'nanika1 nai'
            result_lda = 'nanika2 nai'
            data = None
        except Exception as e:
            print('yoshougai')
            tokens = 'yoshougai nai'
            result_lda = 'yoshougai nai'
            data = None

        data = OrderedDict([
            ('raw', raw_document),
            ('after_analysis', analyzed_document),
            ('result', data),
            ('time_proc', return_ms(time.clock() - t3)),
            ('time_cache_get', return_ms(time_cache_get))
        ])

        return Response(data)


class PredictorView(APIView):
    def get(self, request, format=None):
        t1 = time.clock()
        predictor = cache.get('predictor')
        if predictor:
            cached = True
        else:
            cached = False
        data = OrderedDict([
            ('cached', cached),
            ('time', return_ms(time.clock() - t1))
        ])

        return Response(data)

    def post(self, request, format=None):
        t1 = time.clock()
        upload_predictor()
        return Response({
            ('time', return_ms(time.clock() - t1))
        })


class VectorizerView(APIView):
    def get(self, request, format=None):
        t1 = time.clock()
        predictor = cache.get('vector')
        if predictor:
            cached = True
        else:
            cached = False
        data = OrderedDict([
            ('cached', cached),
            ('time', return_ms(time.clock() - t1))
        ])

        return Response(data)

    def post(self, request, format=None):
        t1 = time.clock()
        upload_vectorizer()
        return Response({
            ('time', return_ms(time.clock() - t1))
        })
