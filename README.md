# Daily Currency exchange rates for South East Asia

url: https://nty-info-center.as.r.appspot.com
<br>
latest exchange rates url: https://nty-info-center.as.r.appspot.com/exchange-rates
<br>

* Compile the app<br>
```python main.py```

* Deploy app to Google Appengine<br>
```gcloud app deploy```

* Browse the website<br>
```gcloud app browse```

* Deploy Datastore indexes based on index.yaml<br>
```gcloud app deploy index.yaml```

* Clean up unused indexes based and keep what's mentioned in index.yaml<br>
```gcloud datastore indexes cleanup index.yaml```

* Install required package <br>
```pip install -r requirements.txt```
