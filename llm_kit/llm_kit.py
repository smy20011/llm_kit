"""Main module."""
import asyncio
import inspect
from functools import wraps, partial

class CompletionEngine:
   async def complete(self, prompt: str) -> str:
      pass


class GPT35CompeleteEngine:
   def __init__(self, clinet = None):
      self.client = client

   async def complete(self, prompt: str) -> str:
      pass

class Prompter:
   def __init__(self, engine: CompletionEngine):
      self.engine = engine


def complete(force_async=False):
   """Wrapper function that turn a prompt function into llm calls"""
   def decorator(func):
      executor = _PromptExecution(func, force_async, [])
      @wraps(func)
      def inner(self, *args, **kwargs):
         return executor(self, *args, **kwargs)
      return inner
   if callable(force_async):
      func = force_async
      force_async = False
      return decorator(func)
   return decorator

class _PromptExecution:
   """Class to execute a LLM prompt"""

   def __init__(self, func, force_async, middlewares):
      self.func = func
      self.middlewares = middlewares
      self.force_async = force_async

   def __call__(self, *args, **kwargs):
      future = self._async_complete(*args, **kwargs)
      if asyncio.iscoroutinefunction(self.func) or self.force_async:
         return future
      event_loop = asyncio.get_event_loop()
      return event_loop.run_until_complete(future)

   async def _async_complete(self, *args, **kwargs):
      prompter = None
      if len(args) > 0:
         prompeter: Prompter = args[0]
      assert isinstance(prompeter, Prompter), "prompt_to_llm can only be used in Prompter class"

      prompt = self.func(*args, **kwargs)
      if asyncio.iscoroutine(prompt):
         prompt = await prompt
      return await self._complete(len(self.middlewares) - 1, prompt, prompeter.engine)


   async def _complete(self, index, prompt, engine):
      if index < 0:
         return await engine.complete(prompt)
      return await self.middlewares[index].apply(partial(self._complete, index - 1), prompt)
