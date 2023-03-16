# Some handy comands in case my python got rusty

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
