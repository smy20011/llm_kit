"""Main module."""

_GLOBAL_LLM_STACK = []

def get_context():
    if len(_GLOBAL_LLM_STACK) == 0:
        raise ValueError("Cannot find LLM context, make sure you run llm functions within context.")
    return _GLOBAL_LLM_STACK[-1]


class LLMContext:

    def __init__(self, **kwargs):
        self._d = {}
        self._d.update(kwargs)


    def __getattribute__(self, name):
        return self._d[name]
