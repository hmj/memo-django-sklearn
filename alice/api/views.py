import time

from collections import OrderedDict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .predictor import default_predict
from .tasks import save_models, upload


class AnalysisView(APIView):
    def get(self, request, format=None):
        t1 = time.clock()
        name = request.GET.get('name', None)

        try:
            res1 = default_predict.analyze(name)
            res2 = default_predict(name)
        except AttributeError as e:
            print(e)
            res1 = 'nanika1 nai'
            res2 = 'nanika2 nai'
        created = default_predict.created

        data = OrderedDict([
            ('raw', name),
            ('after_analysis', res1),
            ('result', res2),
            ('created', created),
            ('time', time.clock() - t1)
        ])

        return Response(data)


class PredictorView(APIView):
    def get(self, request, format=None):
        t1 = time.clock()
        data = OrderedDict([
            ('created', default_predict.created),
            ('time', time.clock() - t1),
            ('dir', dir(default_predict))
        ])

        return Response(data)

    def post(self, request, format=None):
        t1 = time.clock()
        upload()
        return Response({
            'time': time.clock() - t1
        })


class VectorizerView(APIView):
    def get(self, request, format=None):
        return Response({
        })

    def post(self, request, format=None):
        t1 = time.clock()
        save_models()
        return Response({
            'time': time.clock() - t1
        })
