#!/usr/bin/env python

"""Tests for `llm_kit` package."""


import unittest
import asyncio

from llm_kit import CompletionEngine, complete, Prompter, middleware


class FakeEngine(CompletionEngine):
    async def complete(self, prompt: str) -> str:
        await asyncio.sleep(0.01)
        return "Hello World"

class MyTests(unittest.IsolatedAsyncioTestCase):

    async def test_complete_async(self):
        class TestAsyncPrompter(Prompter):
            @complete()
            async def say_hello(self):
                await asyncio.sleep(0.01)
                return "Say hello to the world"
        prompter = TestAsyncPrompter(FakeEngine())
        result = await prompter.say_hello()
        self.assertEqual(result, "Hello World")

    async def test_force_async(self):
        class TestPrompter(Prompter):
            @complete(force_async=True)
            def say_hello(self):
                return "Say hello to the world"
        prompter = TestPrompter(FakeEngine())
        result = await prompter.say_hello()
        self.assertEqual(result, "Hello World")

    def test_complete_sync(self):
        class TestPrompter(Prompter):
            @complete
            def say_hello(self):
                return "Say hello to the world"
        prompter = TestPrompter(FakeEngine())
        result = prompter.say_hello()
        self.assertEqual(result, "Hello World")

    def test_middleware(self):
        @middleware
        async def upper(func, prompt):
            return (await func(prompt)).upper()

        class TestPrompter(Prompter):
            @complete
            @upper
            def say_hello(self):
                return "Say hello to the world"
        prompter = TestPrompter(FakeEngine())
        result = prompter.say_hello()
        self.assertEqual(result, "HELLO WORLD")

    def test_middleware_order(self):
        @middleware
        async def upper(func, prompt):
            return (await func(prompt)).upper()

        class TestPrompter(Prompter):
            @upper
            @complete
            def say_hello(self):
                return "Say hello to the world"
        prompter = TestPrompter(FakeEngine())
        result = prompter.say_hello()
        self.assertEqual(result, "HELLO WORLD")

    def test_middleware_mult(self):
        @middleware
        async def upper(func, prompt):
            return (await func(prompt)).upper()

        @middleware
        async def lower(func, prompt):
            return (await func(prompt)).lower()

        class TestPrompter(Prompter):
            @lower
            @upper
            @complete
            def say_hello(self):
                return "Say hello to the world"
        prompter = TestPrompter(FakeEngine())
        result = prompter.say_hello()
        self.assertEqual(result, "hello world")
