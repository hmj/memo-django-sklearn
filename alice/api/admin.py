from django.contrib import admin
from .models import CountVectorizerParameter, TopicModelParamter

@admin.register(CountVectorizerParameter)
class CountVectorizerParameterAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'parameter_name',
                    'created_at',
                    'enabled',)  # 一覧に出したい項目
    list_display_links = ('id', 'parameter_name',)  # 修正リンクでクリックできる項目
    ordering = ('created_at',)


@admin.register(TopicModelParamter)
class TopicModelParamterAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'parameter_name',
                    'created_at',
                    'enabled',)  # 一覧に出したい項目
    list_display_links = ('id', 'parameter_name',)  # 修正リンクでクリックできる項目
    ordering = ('created_at',)
