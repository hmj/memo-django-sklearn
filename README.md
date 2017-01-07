# memo-django-sklearn

```sh
$ python manage.py migrate
$ python manage.py runserver
```

- POST api/v1/vec
   - CountVectorizerとLDAのモデルをサンプルデータで学習させてシリアライズする
- POST api/v1/pre
  - .pkl ファイルをロードする
- GET api/v1/ana
  - name=
