# Content Creation

techcity does not include any content creation tools in this development stage.
This page contains information to help guide the content creation process.

## Events

In-person events are typically created via fetching,
but it is possible to add events manually
if there is not a data source for generating events.

Importantly,
the event will require an ID in the system.
To produce an ID,
you can use a Python shell.

```
$ python
>>> from techcity.core.ids import generate_id
# In this example, for an old hackathon event, we'll use "2016" as the old ID
# and we provide a *salt* value of "hackathon" to create some uniqueness.
>>> generate_id("2016", "hackathon")
'X3KzWQtv'
```

With this value, create a new event file using `<id>.yaml` as the filename.
Use an alternate event to guide what field values to use for the event data.
