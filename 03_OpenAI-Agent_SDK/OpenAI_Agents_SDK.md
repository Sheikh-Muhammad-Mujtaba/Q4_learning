# OpenAI Agents SDK:

The OpenAI Agents SDK enables developers to build and orchestrate “agentic” AI applications—systems where multiple AI “agents” work together to perform complex, multi-step tasks autonomously in a lightweight, easy-to-use package with very few abstractions.


## 1. Why is the `Agent` class a `dataclass`?

Dataclass is a Python decorator used to automatically add common special methods like `__init__`, `__repr__`, and `__eq__` to classes. It's great for classes that are mainly used to store data.

#### Why use dataclass for Agent?
Because Agent is mostly a container for configuration: like its `name`, `description`, and `instructions` (the system prompt). It doesn’t need a lot of custom logic, just to hold structured data.

### _**Example:**_
```python
from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    instructions: str

# now we can do this
agent = Agent(name="SupportBot", instructions="Be helpful and kind.")
print(agent)

```
Easy to read, clean, and no need to write an `__init__` method!


## 2a. Why are `instructions` (system prompt) in the Agent class, and why can it be a function?

In OpenAI Agents SDK, `instructions` can be a string OR a callable (function) that returns a string. This gives you flexibility.

### _**Example:**_
Sometimes we want static instructions:

```python
agent = Agent(instructions="You are a math tutor.")
```
Other times, we want instructions that change depending on the context or time:

```python
def dynamic_instructions(context):
    return f"You are helping with {context['task']}"

agent = Agent(instructions=dynamic_instructions)
```
So the SDK lets you pass either a string or a function that returns a string depending on the situation.

## 2b. Why is the user prompt passed to the `Runner.run()` method, and why is it a class method?

**The `Runner` class is responsible for executing the agent's logic.**

we give the agent the role and behavior (`instructions`), and the **Runner** is the one that takes a user input and runs the agent.

`run()` is a class method because it doesn't need a Runner object. It just needs:

- the Agent
- the user input

### _**Example:**_
```python
response = Runner.run(agent=my_agent, input="How do I solve x+2=5?")
```
So `run()` is like a **static tool** to run any agent with a given input. It keeps things **modular** and **clean**.


## 3. What is the purpose of the Runner class?
The Runner is like a manager or engine that takes an agent and user input, and runs the logic to get a response.

#### We can Think of it like:
- `Agent` = describes the personality and purpose
- `Runner.run()` = puts that personality into action by talking to the user

We can have multiple runners running different agents with different inputs.

## What are generics in Python, and why use them for `TContext`? Why use `TContext`?
 **Generics = Type placeholders**
They let us write code that works with any type but is still type-safe.

### _**Simple Example:**_
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

box1 = Box        
box2 = Box[str]("hello")   
```

`T` is a placeholder type. Now we can create `Box[int]`, `Box[str]`, etc.

#### **Use of TContext**

In the OpenAI Agents SDK, `TContext` is a generic type for context data that changes depending on the task.

```python
TContext = TypeVar("TContext")
```
So if we’re building a **Travel Agent**, our context might be:

```python
context = {
    "location": "Paris",
    "budget": 1000
}
```
But for a **Medical Agent**, it might be:


By using generics, the SDK can support **any kind of context** while still giving us type safety and auto-complete in IDEs.