# Daily Currency exchange rates for South East Asia

url: https://nty-info-center.as.r.appspot.com
latest exchange rates url: https://nty-info-center.as.r.appspot.com/exchapynges-rates

* Compile the app
```python main.py```

* Deploy app to Google Appengine
```gcloud app deploy```

* Browse the website
```gcloud app browse```

* Deploy Datastore indexes based on index.yaml
```gcloud app deploy index.yaml```

* Clean up unused indexes based and keep what's mentioned in index.yaml
```gcloud datastore indexes cleanup index.yaml```