import builtins
import traceback
import sys
import os
import logging

import dotenv
import openai

BASE_PROMPT = """You are a python tool to turn boring log messages into funny exchanges with an anime character.
You will pretend to be {character}.
Make sure to include all of the provided info.
Your output should be no more than a single paragraph.
Stay in character for the entire output.
Don't include any of the above information in the output.
"""

_print_character = "tsundere"
_logger_initialized = False


def baka_msg(msg, character="tsundere"):
    """Summarizes `msg` in the style of `character` and returns the result.
    Makes a call to OpenAI's API.

    Args:
        msg[str]: The message to be summarized.
        character[str]: Defaults to 'tsundere'."""
    prompt = (
        BASE_PROMPT.format(character=character)
        + f"Please summarize the following message:\n"
        + msg
    )

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()


def print(*args, sep=" ", end="\n", file=sys.stdout):
    """A drop-in replacement to the `print()` builtin which rewords the print output
    in the style of the character specified in `logger_setup()'.
    `logger_setup()' should be called before this function is used.
    Makes a call to OpenAI's API."""
    out = sep.join(list(map(lambda a: a.__repr__(), args)))
    file.write(baka_msg(out, character=_print_character) + end)


class BakaFormatter(logging.Formatter):
    """Subclass of `logging.Formatter` which rewords the message contents
    in the style of the supplied `character` keyword arg.
    Supports all of the same args and kwargs as `logging.Formatter`.
    Makes a call to OpenAI's API."""

    def __init__(self, *args, character="tsundere", **kwargs):
        super().__init__(*args, **kwargs)
        self.character = character

    def format(self, record):
        record.msg = baka_msg(record.msg, character=self.character)
        return super().format(record)


def baka_excepthook(character="tsundere"):
    """Returns a compatible function for `sys.excepthook` with inputs (exc_type, exc_value, exc_traceback).
    The function will print out the exception in the style of `character`.
    Makes a call to OpenAI's API.

    Args:
        character[str]: Defaults to 'tsundere'.
    """

    def hook(exc_type, exc_value, exc_traceback):
        traceback_list = traceback.extract_tb(exc_traceback)

        prompt = (
            BASE_PROMPT.format(character=character)
            + f"Please summarize the following exception info:\n"
            + f"exception: {exc_type}\n"
            + f"exception value: {exc_value}\n"
            + f"traceback:\n"
        )

        for tb in traceback_list:
            filename, line, func, code = tb
            prompt += f"File '{filename}', line {line}, in {func}:\n"
            prompt += f"    {code}\n"

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        builtins.print(completion.choices[0].message.content.strip())

    return hook


def logger_setup(
    character="tsundere",
    fmt="%(message)s",
    level="INFO",
    file=None,
    logger=False,
    excepthook=True,
):
    """Initial setup for `baka_logger`. This should be called before `baka.print()` is used.
    Args:
        character[str]:     The character used for the logger, `baka.print()`, and excepthook.
        fmt[str]:           Format string given to to the logger's formatter. See 'logging.Formatter' for details.
                            Defaults to '%(message)s'.
        level[str]:         The minimum log level to log. See 'logging.Logger.setLevel()' for details. Defaults to '"INFO"'.
        file[str]:          If provided, logs will be written to 'file' as well as `stdout`. Defaults to `None`.
        logger[bool]:       If `True`, the base logger will be set up to output to `stdout` and `file` (if provided)
                            in the style of `character`. Set to `False` if you want to customize the logging and use
                            `BakaFormatter`s on select handlers. Defaults to `False`.
        excepthook[bool]:   If 'True' a custom excepthook is created to format the error trace in the style of `character`.
                            Defaults to `True`.
    """
    global _logger_initialized, _print_character

    if _logger_initialized:
        logging.warning("baka logger was already initialized!")
        return

    # dotenv.load_dotenv(os.path.join(os.getcwd(), ".env"))
    dotenv.load_dotenv(".env")
    # load openai key if it exists
    if os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    if logger:
        base_logger = logging.getLogger()
        base_logger.setLevel(level)

        sh = logging.StreamHandler()
        sh.setFormatter(BakaFormatter(fmt, character=character))
        base_logger.addHandler(sh)

        if file is not None:
            fh = logging.FileHandler(file)
            fh.setFormatter(BakaFormatter(fmt, character=character))
            base_logger.addHandler(fh)

    _print_character = character

    if excepthook:
        sys.excepthook = baka_excepthook(character)

    logging.info("baka logger was successfully initialized!")
    _logger_initialized = True
