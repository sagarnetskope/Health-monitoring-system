# Configure the module according to your needs
from datadog import api,statsd,initialize

options = {
    'api_key':'36304b317c8659644e7f9b48ad556ee6',
    'app_key':'ca05c3abc39f406e4299539d9f6dd449b48c9d16'
}

initialize(**options)

# Use Datadog REST API client
from datadog import api

title = "Something big happened!"
text = 'And let me tell you all about it here!'
tags = ['version:1', 'application:web']

api.Event.create(title=title, text=text, tags=tags)


# Use Statsd, a Python client for DogStatsd
from datadog import statsd

statsd.increment('whatever')
statsd.gauge('foo', 42)