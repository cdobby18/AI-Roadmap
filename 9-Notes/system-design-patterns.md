# System Design — Core Patterns

## Goal
Build the systems vocabulary needed to design, scale, and defend a backend architecture in an interview — before layering AI-specific concerns (prompt engineering, LLM workflows) on top. This is reference material for building visual/slide notes, not a substitute for watching the actual courses.

## What I need to know
- Scaling: vertical vs horizontal, stateless vs stateful services
- Load balancing: algorithms, layer 4 vs layer 7
- Caching: placement, strategies, eviction policies
- CDNs: static content delivery, edge caching
- Databases: replication, sharding/partitioning, indexing, SQL vs NoSQL
- CAP theorem and consistency models (strong vs eventual)
- Message queues and async/event-driven processing
- Microservices vs monolith, API Gateway
- Proxy vs reverse proxy
- Rate limiting / throttling
- Consistent hashing
- Fault tolerance: circuit breakers, retries, timeouts, health checks, failover
- Distributed coordination basics: leader election, heartbeats, quorum
- Observability: logging, metrics, monitoring
- Back-of-envelope capacity estimation

## Key terms
- `vertical scaling`: making one machine bigger (more CPU/RAM). Simple, but has a ceiling and a single point of failure.
- `horizontal scaling`: adding more machines and distributing load across them. Needs statelessness and a load balancer, but scales further.
- `stateless service`: any request can be handled by any server instance because no session/user data is kept in server memory. Required for horizontal scaling to work cleanly.
- `load balancer (LB)`: distributes incoming requests across multiple servers. Layer 4 (routes by IP/TCP, fast, no content awareness) vs Layer 7 (routes by HTTP content — path, headers, cookies — more flexible, slightly slower).
- `round robin / least connections / consistent hashing`: common LB algorithms — round robin cycles evenly, least connections sends to the least busy server, consistent hashing sends the same client/key to the same server (useful for cache locality).
- `reverse proxy`: sits in front of servers, forwards client requests to the right backend (e.g. Nginx). Hides backend topology, can do TLS termination, caching, load balancing.
- `forward proxy`: sits in front of clients, forwards their requests outward (e.g. corporate proxy hiding internal clients from the internet). Opposite direction from reverse proxy.
- `cache`: a fast, small, temporary data store in front of a slower source (DB, API) to reduce latency and load. Lives at multiple layers: client, CDN, app-server, DB.
- `cache-aside (lazy loading)`: app checks cache first; on a miss, reads from DB and writes the result into cache. Most common pattern — cache only holds what's actually been requested.
- `write-through`: app writes to cache and DB at the same time. Cache always fresh, but every write pays the cache-write cost.
- `write-back (write-behind)`: app writes to cache only; cache asynchronously flushes to DB later. Fast writes, but risk of data loss if cache fails before flush.
- `TTL (time to live)`: how long a cached value is considered valid before it's treated as stale and re-fetched.
- `eviction policy`: rule for removing entries when the cache is full — `LRU` (least recently used) and `LFU` (least frequently used) are the common ones.
- `CDN (content delivery network)`: a geographically distributed set of edge servers caching static content (images, video, JS/CSS) close to the user, cutting latency and origin server load.
- `replication`: copying a database across multiple nodes. `master-slave (primary-replica)`: writes go to the primary, reads can be spread across replicas — improves read scaling and durability, adds replication lag.
- `sharding (horizontal partitioning)`: splitting a single dataset across multiple databases/nodes by a key (e.g. user_id range or hash), so each shard holds a subset of rows. Scales write throughput and storage, but makes cross-shard queries/joins hard.
- `partitioning`: splitting data into smaller pieces generally — sharding is one form (across nodes); partitioning can also mean splitting within one DB (e.g. by date range) for query performance.
- `indexing`: a data structure (usually a B-tree) that lets the DB find rows without scanning the whole table. Speeds up reads, costs extra storage and slower writes (index must update too).
- `CAP theorem`: in a distributed system, under a network partition (P) you must choose between Consistency (C, every read gets the latest write) and Availability (A, every request gets a response). You cannot have all three when a partition happens.
- `strong consistency`: every read reflects the most recent write immediately. Simpler to reason about, costs latency/availability.
- `eventual consistency`: reads may return stale data briefly, but all replicas converge eventually. Higher availability/throughput, harder to reason about (used in most NoSQL, DNS, etc.).
- `SQL vs NoSQL`: SQL (Postgres/MySQL) — structured schema, ACID transactions, joins, good for relational integrity. NoSQL (MongoDB, Cassandra, DynamoDB) — flexible schema, built for horizontal scale and high write throughput, weaker consistency guarantees by default.
- `message queue`: a buffer (e.g. RabbitMQ, SQS, Kafka) that decouples producers from consumers — producer pushes a message, consumer processes it independently and asynchronously. Smooths traffic spikes and lets services fail/retry independently.
- `pub/sub (publish-subscribe)`: producers publish events to a topic; any number of subscribers can consume them independently. Used for fan-out (one event, many downstream reactions).
- `API gateway`: a single entry point in front of multiple backend services — handles routing, auth, rate limiting, and request/response transformation so clients don't talk to each microservice directly.
- `microservices vs monolith`: monolith = one deployable app, simple to build/deploy early, harder to scale specific parts independently. Microservices = independently deployable services per domain, scale/deploy independently, but add network, consistency, and operational complexity.
- `rate limiting / throttling`: capping how many requests a client can make in a window (e.g. token bucket, leaky bucket algorithms) to protect the system from abuse or overload.
- `consistent hashing`: a hashing scheme where adding/removing a node only remaps a small fraction of keys (not all of them), used for cache/shard node distribution so scaling out doesn't invalidate everything.
- `circuit breaker`: stops calling a dependency that's already failing (after N failures, "open" the circuit and fail fast) instead of piling up timeouts, then periodically retries ("half-open") to see if it's recovered.
- `retry with backoff`: retrying a failed request, but waiting longer between each attempt (often exponential) to avoid hammering a struggling service.
- `timeout`: a hard limit on how long to wait for a response before giving up — prevents one slow dependency from cascading into total system failure.
- `health check`: an endpoint/probe a load balancer or orchestrator polls to know if an instance is alive and should keep receiving traffic.
- `failover`: automatically switching to a backup/replica when the primary fails, to keep the system available.
- `leader election`: in a cluster of nodes, a protocol (e.g. Raft, Paxos) to agree on which single node is "in charge" of coordinating writes/decisions, so the group doesn't need a human to pick.
- `quorum`: minimum number of nodes that must agree/respond for a read or write to be considered successful — balances consistency and availability in replicated systems.
- `back-of-envelope estimation`: quick math (requests/sec, storage/day, bandwidth) used in interviews to size a system before designing it — order-of-magnitude, not precision.

## When to use
- Reach for horizontal scaling + a load balancer once a single server can't handle load or you need redundancy — but only after the service is stateless.
- Use cache-aside as the default caching strategy unless you specifically need cache and DB to never diverge (then write-through) or need very fast writes with tolerance for some loss (write-back).
- Put a CDN in front of anything static (images, JS bundles, video) — never serve those directly from your app server.
- Shard a database when a single node can no longer hold the write throughput or storage of one growing table; replicate first for read scaling and durability before reaching for sharding (sharding is harder to undo).
- Choose SQL when you need relational integrity/transactions (payments, orders); choose NoSQL when you need flexible schema and horizontal write scale (activity feeds, logs, sessions).
- Use a message queue whenever a task doesn't need an immediate response (sending email, processing an upload, retraining a model) — decouple it instead of making the client wait.
- Use an API gateway once you have more than one backend service and want a single place to enforce auth/rate limiting instead of repeating it per service.
- Use a circuit breaker + retry with backoff around any call to an external dependency (another service, a third-party API, an LLM provider) that can be slow or flaky.
- Use consistent hashing whenever nodes will be added/removed dynamically (autoscaling cache or shard nodes) and you want to avoid a full remap on every scaling event.
- Favor eventual consistency (and accept it) for things users don't need instantly-fresh (like counts, feeds); require strong consistency for money, inventory, and anything where a stale read causes a real error.

## Interview review
- If asked "how would you scale this," the expected shape of answer is: identify the bottleneck first (reads? writes? compute?), then apply the matching pattern — don't jump straight to "add more servers."
- Be ready to explain CAP theorem with a concrete example: during a network partition, do you serve possibly-stale data (choose A) or refuse to serve until consistency is restored (choose C)? Most real systems pick availability with eventual consistency, and explicitly call out where they need strong consistency instead (e.g. payments).
- When asked to design a caching layer, mention cache-aside as default, then justify TTL and eviction policy (LRU is the standard first answer) based on access patterns.
- If asked about database scaling, sequence your answer: indexing → read replicas → caching → sharding — sharding is the last resort because it's the hardest to reverse and complicates queries.
- Be ready to draw (or describe) request flow end to end: client → CDN/reverse proxy → load balancer → app servers → cache → database (with replicas/shards), including where a message queue sits for async work.
- If asked about failure handling, mention timeouts + retries + circuit breakers together — timeouts alone without circuit breakers still let failures cascade.
- Know the tradeoff questions cold: SQL vs NoSQL, strong vs eventual consistency, monolith vs microservices, sharding vs replication, layer 4 vs layer 7 load balancing. Each has a "it depends on X" answer — interviewers are testing whether you know what X is, not that you picked the "right" side.

## Common pitfalls
- Adding more servers before making the service stateless — a stateful service can't be horizontally scaled correctly regardless of how many instances you run.
- Reaching for sharding before trying replication + caching + indexing — sharding adds permanent complexity (cross-shard joins, rebalancing) that's hard to undo.
- Caching everything with no TTL/eviction policy, leading to stale data serving indefinitely or unbounded memory growth.
- Treating "eventual consistency" as an excuse to ignore consistency entirely — you still need to reason about which operations truly tolerate staleness.
- Adding retries without backoff or without a circuit breaker — this can turn one slow dependency into a self-inflicted traffic spike ("retry storm") that makes the outage worse.
- Designing microservices before there's an actual reason to split (team boundaries, independent scaling needs) — premature microservices mostly just add network calls and deployment overhead.
- Forgetting health checks, so a load balancer keeps sending traffic to a dead instance until a request actually times out.
- Skipping back-of-envelope math in an interview and jumping straight to a diagram — interviewers want to see you size the problem first (requests/sec, data volume) so your design choices are justified, not guessed.

## How to use (patterns as diagrams / pseudocode)

### Basic request flow
```
Client
  │
  ▼
CDN (static assets, cached at edge)
  │
  ▼
Reverse Proxy / Load Balancer  ──►  App Server 1
  │                              ──►  App Server 2
  │                              ──►  App Server 3
  ▼
Cache (Redis)  ◄──miss──  App Server  ──►  Database (primary)
                                              │
                                              ▼
                                        Read Replicas
```

### Cache-aside pattern
```
def get_user(user_id):
    value = cache.get(user_id)
    if value is None:               # cache miss
        value = db.query(user_id)
        cache.set(user_id, value, ttl=300)
    return value                    # cache hit or freshly loaded
```

### Circuit breaker (state machine)
```
CLOSED (calls pass through)
   │  failures >= threshold
   ▼
OPEN (calls fail immediately, no network call made)
   │  after cooldown timer
   ▼
HALF-OPEN (allow one trial call)
   │success            │failure
   ▼                   ▼
CLOSED              OPEN (reset cooldown)
```

### Consistent hashing (ring)
```
        node A
      /         \
node D            node B
      \         /
        node C

key "user:123" -> hash -> lands between node B and node C
                        -> stored on node C (next node clockwise)

Adding node E only remaps keys between E and its counter-clockwise
neighbor — the rest of the ring is untouched.
```

### Message queue / async processing
```
Producer (API request)
   │  publish "resize_image" event
   ▼
Queue (SQS / RabbitMQ / Kafka)
   │
   ▼
Consumer worker(s)  ──►  process image  ──►  write result to DB/S3

Client gets an immediate "202 Accepted" instead of waiting
for the resize to finish.
```

### Database read replica routing
```
def route_query(query):
    if query.is_write:
        return primary_db.execute(query)
    else:
        return random.choice(read_replicas).execute(query)
```

### Back-of-envelope estimation (template)
```
1. Users: total users, daily active users (DAU)
2. Requests/sec: DAU * avg actions per user / 86400 seconds
3. Storage/day: requests/day * avg payload size
4. Storage/year: storage/day * 365 (adjust for retention policy)
5. Bandwidth: requests/sec * avg payload size

Keep it order-of-magnitude — round aggressively, state assumptions
out loud, and use the numbers to justify design choices
(e.g. "10K req/sec means we need a load balancer + caching, not
just a bigger single server").
```
