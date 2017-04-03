from datadog import initialize, api
import time

options = {
    'api_key': '36304b317c8659644e7f9b48ad556ee6',
    'app_key': 'd4e3bd57c2f3f793a31e47eda2f531bb8381c060'
}

initialize(**options)

now = time.time()
future_10s = now + 10

# Submit a single point with a timestamp of `now`
api.Metric.send(metric='system.cpu.idle', points=1000)