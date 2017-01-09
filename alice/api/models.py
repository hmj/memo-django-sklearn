from django.db import models
from django.utils import timezone


class TopicModelParamter(models.Model):
    """
    トピックモデルの学習パラメータ
    """
    TYPE_METHOD_DEFAULT = 'online'
    TYPE_METHOD_CHOICE = (
        ('online', 'online'),
        ('batch', 'batch'),
    )

    id = models.AutoField(primary_key=True)
    parameter_name = models.CharField('name', max_length=255, blank=False)
    n_topics = models.IntegerField('トピック数')
    max_iter = models.IntegerField('max_iter')

    learning_method = models.CharField('learning_method',
                                       choices=TYPE_METHOD_CHOICE,
                                       default=TYPE_METHOD_DEFAULT,
                                       max_length=128
                                       )
    learning_offset = models.FloatField('learning_offset')
    random_state = models.IntegerField('random_state')
    n_jobs = models.IntegerField('n_jobs')
    verbose = models.IntegerField('verbose')
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField('作成日時', default=timezone.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        db_table = 'topic_model_parameter'
        ordering = ('created_at', 'enabled', 'id',)

    def __repr__(self):
        return "{}: {}".format(self.id, self.parameter_name)

    __str__ = __repr__

    @classmethod
    def get_params(cls):
        leaning_columns = ('n_topics', 'max_iter', 'learning_method', 'learning_offset', 'random_state', 'n_jobs', 'verbose',)
        obj = cls.objects.filter(enabled=True).first()
        return {k: obj.__dict__.get(k) for k in leaning_columns}

class CountVectorizerParameter(models.Model):
    id = models.AutoField(primary_key=True)
    parameter_name = models.CharField('name', max_length=255, blank=False)
    max_df = models.FloatField('max_df')
    min_df = models.IntegerField('min_df')
    max_features = models.IntegerField('max_features')
    stop_words = models.CharField('stop_words', max_length=255, blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField('作成日時', default=timezone.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        db_table = 'count_vectorizer_parameter'
        ordering = ('created_at', 'enabled', 'id',)

    def __repr__(self):
        return "{}: {}".format(self.id, self.parameter_name)

    __str__ = __repr__

    @classmethod
    def get_params(cls):
        leaning_columns = ('max_df', 'min_df', 'max_features', 'stop_words',)
        obj = cls.objects.filter(enabled=True).first()
        return {k: obj.__dict__.get(k) for k in leaning_columns}
