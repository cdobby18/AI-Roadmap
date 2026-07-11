"""
Load Balancer Strategies — guided exercise.

Theory: Notes/system-design-patterns.md -> "load balancer (LB)",
"round robin / least connections / consistent hashing".

A load balancer's core job is one decision, repeated: "which server gets
this request?" Different algorithms answer it differently, and interviews
love asking when each one breaks down. This exercise makes the difference
observable instead of theoretical.

YOUR TASK — implement two strategies:

1. RoundRobinBalancer.pick(): cycle through servers in order — s1, s2, s3,
   s1, s2, s3, ... regardless of how busy each server is. Simple and fair
   ONLY when requests are uniform.

2. LeastConnectionsBalancer.pick(): return the server with the fewest
   `active` connections right now (ties: first in list order). This is what
   you want when request durations vary wildly — exactly the case with LLM
   calls, where one request streams for 30s while another finishes in 200ms.

Both must:
- pick from `self.servers` (list of Server objects)
- call `server.begin()` on the chosen server before returning it
  (the caller later calls `server.end()` when the request finishes).

Hints:
- Round robin needs one integer of state; modulo does the wrap-around.
- Least connections is a min() with the right key — but the tie-break
  ("first in list order") matters for the test, and min() already behaves
  that way for equal keys.

Run `python 05-load-balancer.py` until the self-test passes.
"""


class Server:
    def __init__(self, name: str):
        self.name = name
        self.active = 0      # requests currently in flight
        self.handled = 0     # total requests ever assigned

    def begin(self):
        self.active += 1
        self.handled += 1

    def end(self):
        self.active -= 1

    def __repr__(self):
        return f"Server({self.name}, active={self.active}, handled={self.handled})"


class RoundRobinBalancer:
    def __init__(self, servers: list):
        self.servers = servers
        # TODO: your cursor state here

    def pick(self) -> Server:
        raise NotImplementedError("implement me — see module docstring")


class LeastConnectionsBalancer:
    def __init__(self, servers: list):
        self.servers = servers

    def pick(self) -> Server:
        raise NotImplementedError("implement me — see module docstring")


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # --- Round robin: strict rotation, blind to load -----------------------
    servers = [Server("s1"), Server("s2"), Server("s3")]
    rr = RoundRobinBalancer(servers)

    order = [rr.pick().name for _ in range(7)]
    assert order == ["s1", "s2", "s3", "s1", "s2", "s3", "s1"], f"got {order}"

    # --- Least connections: routes around busy servers ----------------------
    servers = [Server("s1"), Server("s2"), Server("s3")]
    lc = LeastConnectionsBalancer(servers)

    # First three picks spread across all idle servers (each pick makes the
    # chosen server busier, so the next pick must go elsewhere).
    first_three = {lc.pick().name for _ in range(3)}
    assert first_three == {"s1", "s2", "s3"}, f"idle servers should each get one: {first_three}"

    # s1 and s2 finish; s3 is still holding its (slow) request.
    s1, s2, s3 = servers
    s1.end(); s2.end()

    # Now the balancer must avoid s3 while it's busy.
    p1, p2 = lc.pick(), lc.pick()
    assert s3 not in (p1, p2), "least-connections must avoid the busy server"

    # Everyone finishes; ties break by list order.
    for s in servers:
        while s.active:
            s.end()
    # All at 0 active -> min() tie-break gives the first server in the list.
    assert lc.pick().name == "s1", "ties must break in list order"

    # --- The scenario that separates them -----------------------------------
    # One server gets stuck with a long request. Round robin keeps feeding it;
    # least connections doesn't.
    servers = [Server("s1"), Server("s2")]
    lc = LeastConnectionsBalancer(servers)
    stuck = lc.pick()          # this request never finishes (no .end())
    other = [s for s in servers if s is not stuck][0]

    for _ in range(4):         # four quick requests: begin then immediately end
        s = lc.pick()
        assert s is other, "quick requests must all route around the stuck server"
        s.end()

    print("✅ all load-balancer tests passed")
