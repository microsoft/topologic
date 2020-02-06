# Enabling Logging with `topologic`

To get access to logging in topologic, the user needs to setup a log handler and log formatter.

## Example
You can add the snippet below to your script that will log the 'DEBUG' log level (and above) to the console.::

```python
import logging

logger = logging.getLogger()
handler = logging.StreamHandler() #  stream handler will log to the console
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)  # will log DEBUG and above log levels to the specified handler
```

## Common Logging Problems
The `logging` module is set up to allow libraries to register log entries as per the final user's configuration, by 
not specifying any handlers or formatters, but allowing the library user to specify their own as they see fit.  

Some Python libraries break this expectation by setting their own handlers, formatters, or debugging level, resulting
in duplicate log messages output.  If this situation occurs, you can address this by the following snippet:

```python
import logging
logger = logging.getLogger()
logger.handlers = []  # this removes all handlers in the root logger
# set your own handler and formatter as per the example above
``` 

## See also

There are other types of logging handlers that may be of use to you, in particular, the FileHandler.
For more information on handlers see: https://docs.python.org/3.6/library/logging.handlers.html

The logging hierarchy is `CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET`. If you want the most verbose logging available for
topologic, set your logger level to NOTSET.
For more information on log levels see: https://docs.python.org/3.6/library/lDEBUGogging.html#logging-levels
