# Baka Logger
`baka_logger` turns your boring log messages into fun interactions with anime characters.


```python
from baka_logger import logger_setup

logger_setup()

1/0
```

```
Hmph, what a useless error. I can't believe someone as great as me has to deal with such trivial matters.
Apparently, some fool tried to divide by zero, causing this <class 'ZeroDivisionError'>. Can't they see
that's impossible? I mean, the traceback says it all. It happened in '/home/qferbs/code/baka_logger/example.py',
line 5. How shameful. Next time, they should think before they try something so stupid.
```


It also integrates with Python's standard `logging` library:
```python
from baka_logger import logger_setup
import logging

logger_setup(character="Asuka", fmt="%(asctime)s - %(levelname)s - %(message)s", file="log.out", logger=True)

logging.warning("The program has crashed")
```

```
2023-03-12 21:06:40,841 - INFO - Ugh, finally that baka logger is up and running. At least it won't be
as useless as Shinji.
2023-03-12 21:06:47,172 - WARNING - Ugh, what did you do now? Did you break it again? I swear, it's like
you have no idea what you're doing! This program has totally crashed, just like your love life. Get it
together, or else you'll be as useful as Rei on a bad day.
```

```
# log.out
2023-03-12 21:06:40,841 - INFO - Ugh, finally that baka logger is up and running. At least it won't be
as useless as Shinji.
2023-03-12 21:06:47,172 - WARNING - Ugh, what did you do now? Did you break it again? I swear, it's like
you have no idea what you're doing! This program has totally crashed, just like your love life. Get it
together, or else you'll be as useful as Rei on a bad day.
```

You can even override the default `print()` statement to give you much more descriptive outputs:
```python
from baka_logger import logger_setup, print

logger_setup(character="Bocchi the Rock having a breakdown")

print("baka_logger is my favorite Python package!")
```

```
*Uncontrollable sobbing* Ahh! Why can't I be everyone's favorite Python package? *sniffles* It's not fair,
Bocchi the Rock just can't compete with baka_logger. *more crying* Why do I even try? *sobs*
```

## Installation
Installation is as simple as:
```console
pip install baka_logger
```

`baka_logger` requires an OpenAI API key to function. See https://openai.com/blog/openai-api if you don't have one.
By default the API key be will read out of a `.env` file  like so:
```
# .env
OPENAI_API_KEY=<your-api-key>
```

You can also assign the key yourself by setting:
```python
import openai
openai.api_key="<your-api-key>"
```
before calling `baka_logger.logger_setup()`.
