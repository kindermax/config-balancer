# Config balancer
- Basic interactive usage:

```
user# python3 main.py
> print
Current config:
{}
> add server
> server name: srv1
> add service
> service name: flask
> services amount: 10
> print
Current config:
{'srv1': {'flask': 10}}
> add server
> server name: srv2
> print
Current config:
{'srv1': {'flask': 10}, 'srv2': {}}
> add service
> service name: django
> services amount: 5
> print
Current config:
{'srv1': {'flask': 10}, 'srv2': {'django': 5}}
> save
> exit
user#
```
