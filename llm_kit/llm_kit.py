"""Main module."""
import asyncio
import inspect
from functools import wraps

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
      is_func_async = inspect.iscoroutinefunction(func)

      async def async_inner(self: Prompter, *args, **kwargs) -> str:
         assert isinstance(self, Prompter), "prompt_to_llm can only be used in Prompter class"
         prompt = func(self, *args, **kwargs)
         if asyncio.iscoroutine(prompt):
            prompt = await prompt
         return await self.engine.complete(prompt)

      def sync_inner(self: Prompter, *args, **kwargs) -> str:
         event_loop = asyncio.get_event_loop()
         return event_loop.run_until_complete(async_inner(self, *args, **kwargs))

      if inspect.iscoroutinefunction(func) or force_async:
         return wraps(func)(async_inner)
      else:
         return wraps(func)(sync_inner)
   return decorator
