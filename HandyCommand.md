# Some handy comands in case my python got rusty

* Compile the app<br>
```python main.py```

*  Initiates an authentication flow to obtain credentials for accessing Google Cloud resources. When you run this command, you will be prompted to sign in to your Google account and grant permissions to the SDK to access your account information. Once you have successfully authenticated, the SDK will store your credentials locally and use them to authorize subsequent commands.
```gcloud auth login```

* List all the projects associated with your Google Cloud account.
```gcloud projects list```

* Deploy app to Google Appengine<br>
```gcloud app deploy```

* Browse the website<br>
```gcloud app browse```

* Deploy Datastore indexes based on index.yaml<br>
```gcloud app deploy index.yaml```

* Clean up unused indexes based and keep what's mentioned in index.yaml<br>
```gcloud datastore indexes cleanup index.yaml```

* List my index
```gcloud datastore indexes list```

* Install required package <br>
```pip install -r requirements.txt```
