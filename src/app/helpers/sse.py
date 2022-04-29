# format_sse is NOT used if using flask-sse
def format_sse(data: str, event=None) -> str:
    """Formats a string and an event name in order to follow the event stream convention.
    >>> format_sse(data=json.dumps({'abc': 123}), event='Jackson 5')
    'event: Jackson 5\\ndata: {"abc": 123}\\n\\n'
    """

    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg
