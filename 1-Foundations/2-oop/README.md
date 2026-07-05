# 2 · OOP

Classes, instances, and the four pillars (encapsulation, inheritance, polymorphism, abstraction). One-Piece-themed examples throughout — Devil Fruits, Pirates, Marines — but the mechanics are the same OOP you'll use in every `class` you write for APIs and ML pipelines later.

---

## Progress Checklist

- [x] `class1.py` — classes & instances: `__init__`, attributes, methods, `self` (with inline notes recapping the vocabulary)
- [x] `class2.py` — class variables (`numOfEmps`, `raise_amount`) vs instance variables — shared state vs per-object state
- [x] `class3.py` — `@classmethod` (alternative constructor via `from_string`), `@staticmethod` (`is_workday`, no `self`/`cls` needed)
- [x] `class4.py` — inheritance: `Character` base class → `Pirate` / `Marine` / `Revolutionary` subclasses, `super().__init__()`, method overriding
- [x] `class5.py` — dunder methods: `__str__`, `__repr__`, `__add__`, `__len__`, `__eq__`, `__lt__` (the last enables `list.sort()`)
- [x] `class6.py` — property decorators: `@property` getter, `@x.setter`, `@x.deleter`
- [x] `oop.py` — capstone: all four pillars in one file — `ABC`/`@abstractmethod` (abstraction), `Student`/`Teacher(Person)` (inheritance + polymorphism via overridden `role()`), `BankAccount.__balance` (encapsulation via name-mangled private attribute)

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `self` | The instance calling the method — always the first parameter |
| `super().__init__()` | Calls the parent constructor so subclasses don't repeat setup logic |
| `@classmethod` | Takes `cls` instead of `self` — common use: alternative constructors |
| `@staticmethod` | No implicit first argument — a plain function that just lives in the class namespace |
| `__str__` vs `__repr__` | `__str__` is for humans (`print(obj)`), `__repr__` is for developers/debugging |
| `@property` | Lets a method be accessed like an attribute (`obj.fullname` not `obj.fullname()`) |
| `_protected` / `__private` | Convention (`_x`) vs name-mangled (`__x`) — Python doesn't truly enforce privacy either way |

---

## The Four Pillars — Where to Find Them

| Pillar | File | Example |
|--------|------|---------|
| Encapsulation | `oop.py` | `BankAccount.__balance` — only touchable via `deposit`/`withdraw`/`get_balance` |
| Inheritance | `class4.py`, `oop.py` | `Pirate(Character)`, `Student(Person)` |
| Polymorphism | `class4.py`, `oop.py` | Each subclass overrides `show_info()` / `role()` differently |
| Abstraction | `oop.py` | `Person(ABC)` with `@abstractmethod role()` — can't instantiate `Person` directly |
