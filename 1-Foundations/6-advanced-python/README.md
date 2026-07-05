# 6 · Advanced Python

Two nested subfolders: `asyncio/` (concurrency) and `modules/` (imports, file I/O, small self-contained scripts). asyncio is the one that matters most going forward — production AI apps almost always need to run multiple I/O-bound calls (LLM requests, DB queries) concurrently instead of one at a time.

---

## Progress Checklist

### asyncio/
- [x] `coroutine.py` — `async def` + `await`: a single coroutine (`fetch_data`) run via `asyncio.run(main())`
- [x] `tasks.py` — two coroutines awaited back to back — see Gotcha below
- [x] `future.py` — `asyncio.Future`: a low-level awaitable manually resolved with `future.set_result()` from a separate task
- [x] `synchro.py` — `asyncio.Lock` guarding a shared counter across 5 concurrent coroutines (`asyncio.gather`) — prevents race conditions on `shared_resource`
- [x] `taskGroup.py` — `asyncio.TaskGroup` (3.11+): the modern structured-concurrency API — spawn multiple tasks, group errors, collect `.result()` from each

### modules/
- [x] `example_module.py` + `mainModule.py` — the actual import pair: `example_module.py` defines `add()`, `mainModule.py` does `import example_module` and calls it — the minimal example of splitting code across files
- [x] `functions.py` — a plain function + call, no default param
- [x] `defaultParam.py` — default parameter values (`name="Guest"`), a function returning multiple values (`return total, count, avg` → tuple unpacking), `if __name__ == "__main__":` guard, and reading input via `input()`
- [x] `textFile.py` — `open(path, "w")` / `open(path, "r")` with the `with` context manager for plain text
- [x] `JSON.py` — `json.dump()` to write a dict to a file, `json.load()` to read it back
- [x] `APIReq.py` — combines modules + `requests`: calls the public `agify.io` API to predict an age from a name, wrapped in a `get_age_prediction()` function plus a `main()` entry point

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `async def` / `await` | Defines a coroutine / pauses it until the awaited thing resolves |
| `asyncio.create_task()` | Schedules a coroutine to run concurrently — just calling/awaiting it directly does **not** make it concurrent |
| `asyncio.gather(*coros)` | Runs multiple coroutines concurrently and waits for all of them |
| `asyncio.TaskGroup` | Structured concurrency — auto-cancels sibling tasks if one raises, cleaner than bare `gather` |
| `asyncio.Lock` | Prevents two coroutines from mutating shared state at the same time |
| `if __name__ == "__main__":` | Only run this block when the file is executed directly, not when imported |

---

## Gotcha

`tasks.py` creates two coroutine objects (`fetch_data(2,1)`, `fetch_data(2,2)`) and then `await`s them one after another — that's **sequential**, not concurrent, so total runtime is the sum of both delays (~4s). To actually run them concurrently you need `asyncio.create_task()` (or `asyncio.gather`, as in `synchro.py`) so both `sleep`s overlap — compare against `taskGroup.py`, which does this correctly and finishes in the time of the *slowest* task (~3s), not the sum.
