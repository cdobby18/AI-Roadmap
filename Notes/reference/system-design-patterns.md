# System Design — Core Patterns

> The vocabulary to design, defend, and scale a backend architecture. Not a substitute for practicing whiteboard design, but the reference for the patterns interviewers expect you to know.

---

## 1. Scaling

**Vertical vs Horizontal:**
- **Vertical** (scale up): Bigger machine. Simple, has a ceiling, creates a single point of failure.
- **Horizontal** (scale out): More machines. Needs stateless services and a load balancer. Scales further, but adds complexity (distributed state, coordination).

**Stateless vs Stateful:**
- **Stateless:** Any server can handle any request. No session data in local memory. Required for horizontal scaling.
- **Stateful:** Server remembers client state between requests (e.g., WebSocket connections, in-memory sessions). Harder to scale — needs sticky sessions or external state store (Redis).

## 2. Load Balancing

**Layer 4 (Transport):** Routes by IP + TCP port. Fast, no content awareness. Can't make application-level routing decisions.

**Layer 7 (Application):** Routes by HTTP content (path, headers, cookies, body). More flexible — can route `/api/v1` to one service and `/api/v2` to another. Slightly slower.

**Algorithms:**
- **Round robin:** Cycles evenly across servers. Simple, doesn't account for load.
- **Least connections:** Sends to the server with fewest active connections. Better for variable-length requests.
- **Consistent hashing:** Same client/key always goes to the same server. Useful for cache locality — minimizes cache misses on server changes.

## 3. Caching

**Where caches live:** Client (browser cache), CDN (edge cache), app server (in-memory cache like Redis), database (buffer pool). Cache at the level closest to the bottleneck.

**Patterns:**
- **Cache-aside (lazy loading):** App checks cache first. On miss: reads from DB, writes result to cache. Most common pattern. Cache only holds what's actually been requested. Downside: cache miss penalty (DB read + cache write).
- **Write-through:** App writes to cache AND DB simultaneously. Cache always consistent. Every write pays double latency.
- **Write-behind (write-back):** App writes to cache only; cache asynchronously flushes to DB. Fast writes. Risk: data loss if cache fails before flush.

**Eviction policies:**
- **LRU (Least Recently Used):** Evict items not accessed for the longest time. Most common. Good for most workloads.
- **LFU (Least Frequently Used):** Evict items accessed least often. Good for workloads with stable popularity patterns (some items accessed far more than others).
- **TTL (Time To Live):** Items expire after a fixed duration. Simple, predictable. Used when data is known to be stale after a certain time (e.g., weather data).

**When to cache:** Data that is read frequently, written infrequently, and can tolerate some staleness. Never cache data that must be instantly consistent (financial transactions, real-time inventory).

## 4. CDN

A geographically distributed set of edge servers that cache static content (images, CSS, JS, video) close to users. Reduces latency and offloads origin servers. Use for any globally-distributed application with static assets.

## 5. Databases

**Replication (Primary-Replica):** Writes go to primary; reads can be spread across replicas. Improves read throughput and durability. Replication lag means replicas may be slightly stale. If primary fails, a replica must be promoted — downtime during failover.

**Sharding (Horizontal Partitioning):** Split data across multiple database nodes by a shard key (e.g., `user_id % N`). Each node holds a subset of rows. Scales write throughput and storage. Makes cross-shard queries and joins expensive or impossible. Choosing a good shard key is critical — a bad key causes hot spots.

**Indexing:** B-tree structure that enables O(log n) lookups instead of O(n) full table scans. Add indexes on columns used in WHERE, JOIN, ORDER BY. Cost: ~20% storage overhead, slower writes (index must be updated). Don't index low-cardinality columns (booleans, status fields with few values) or write-heavy tables.

**SQL vs NoSQL:**
| Need | Choice |
|---|---|
| Complex joins, ACID transactions, structured schema | SQL (PostgreSQL) |
| Flexible schema, rapid iteration | NoSQL (MongoDB) |
| High write throughput at scale | NoSQL (Cassandra, DynamoDB) |
| Document/JSON with queries | PostgreSQL (JSONB) |
| Vector search | pgvector or specialized (Pinecone, Weaviate) |

**Denormalization:** Storing redundant data (e.g., storing user name in the orders table instead of joining on user_id). Tradeoff: faster reads (no join), but must keep redundant copies in sync. Common in NoSQL and read-heavy systems.

## 6. CAP Theorem

In a distributed system, during a network partition (P), you must choose between:
- **Consistency (C):** Every read gets the latest write. System may reject requests until partition is resolved (downtime).
- **Availability (A):** Every request gets a response, even if that response returns stale data.

You cannot have all three simultaneously when a partition occurs. In practice: choose CP (banking, financial data) or AP (social media, content delivery). Most systems are AP with eventual consistency.

**Consistency models:**
- **Strong:** Every read sees the most recent write. Simplest to reason about. Highest latency. Used in: financial systems, inventory.
- **Eventual:** Reads may return stale data, but replicas converge over time. Used in: DNS, social media feeds, content delivery.
- **Read-your-writes:** User sees their own writes immediately, but others may not. Common compromise for user-facing applications.

## 7. Message Queues

Decouple producers (who send events) from consumers (who process them). The queue buffers between them, handling traffic spikes and allowing independent scaling.

**Use cases:**
- Async processing: "User uploaded a file" → queue → process → notify.
- Decoupling services: Order service doesn't need to wait for email service.
- Smoothing traffic spikes: Queue absorbs bursts, consumers process at their own pace.
- Retry/error handling: Failed messages go to a dead-letter queue for later inspection.

**Kafka vs RabbitMQ vs SQS:**
- **Kafka:** High throughput, durable, replayable (messages persist). Best for event streaming and data pipelines.
- **RabbitMQ:** Low latency, flexible routing. Best for task distribution and RPC-style messaging.
- **SQS:** Fully managed AWS, no ops. Best for simple use cases within AWS.

## 8. Microservices vs Monolith

**Monolith:** Single deployable unit. Simple to develop, test, and deploy in early stages. Becomes a bottleneck as the team and codebase grow.

**Microservices:** Independently deployable services, each owning its data. Pros: independent scaling, team autonomy, technology flexibility. Cons: distributed system complexity (network calls, data consistency, service discovery, testing).

**API Gateway:** A single entry point that routes requests to the appropriate microservice. Handles authentication, rate limiting, logging, and request transformation. Clients talk to the gateway, not to individual services.

**When to start with microservices:** Never. Start monolith, extract services when the monolith's boundaries are well-understood (Conway's Law — architecture mirrors communication structure).

## 9. Proxy vs Reverse Proxy

**Forward proxy:** Sits in front of clients, forwards their requests outward. Used for: content filtering, hiding client IPs, bypassing geo-restrictions.

**Reverse proxy:** Sits in front of servers, forwards client requests to the right backend (Nginx, Caddy, Traefik). Used for: load balancing, TLS termination, caching, hiding backend topology.

## 10. Rate Limiting

Cap requests per client per time window. Essential for public APIs to prevent abuse and control costs.

**Algorithms:**
- **Token bucket:** Tokens added at a fixed rate. Each request consumes a token. Allows bursts up to bucket size.
- **Leaky bucket:** Requests processed at a fixed rate. Excess is queued or dropped. Smoother output but less burst-tolerant.
- **Sliding window log:** Track timestamps of last N requests within a time window. Most accurate, most memory.
- **Sliding window counter:** Approximate version using counters per bucket. Good balance of accuracy and memory.

**Where to rate limit:** API gateway (global), per-endpoint (inference costs more than health check), per-user (prevent abuse).

## 11. Consistent Hashing

A distribution scheme where adding/removing servers only causes remapping of 1/N of keys (instead of nearly all keys in simple hash modulo). Used in: distributed caches (Redis Cluster), load balancers (for cache affinity), distributed databases.

**How it works:** Servers and keys are placed on a hash ring. Each key is assigned to the nearest server clockwise. When a server is added/removed, only the keys between it and its neighbor are remapped.

## 12. Fault Tolerance

- **Circuit breaker:** After N consecutive failures, stop calling the service and fail fast (or return cached response) for a cooldown period. Prevents cascading failures and gives the downstream service time to recover.
- **Retry with exponential backoff + jitter:** Retry on transient failures, doubling wait time between retries. Add random jitter to prevent thundering herd (all clients retrying simultaneously).
- **Timeout:** Set a maximum wait time for every external call. Without this, a slow downstream service consumes resources indefinitely.
- **Health checks:** Endpoints that tell load balancers whether a service instance is healthy. Kill unhealthy instances.
- **Graceful degradation:** Feature reduces functionality instead of failing completely. Example: if recommendation service is down, show popular items instead.
- **Bulkhead:** Isolate resources per service/tenant so a failure in one doesn't exhaust shared resources. Named after ship compartments — if one compartment floods, the ship stays afloat.
- **Dead letter queue:** Failed messages go here for later analysis instead of being lost. Without this, transient failures cause permanent data loss.

## 13. Observability

**Three pillars:**
- **Logging:** Structured events (JSON) recording what happened. Use for debugging and auditing. Centralize logs (Elasticsearch, Loki, CloudWatch).
- **Metrics:** Numerical measurements over time (request rate, error rate, latency P50/P95/P99, CPU/memory usage). Use for alerting and capacity planning. Tools: Prometheus, Grafana, Datadog.
- **Tracing:** Track a single request across multiple services. Shows where time is spent and where failures occur. Tools: Jaeger, Zipkin, OpenTelemetry.

**Key metrics to track:**
- **Latency percentiles:** P50 (median), P95 (almost everyone), P99 (worst case). Average latency hides bad outliers. P99 is what users actually experience.
- **Error rate:** Percentage of requests returning 5xx or application errors. Alert on >1%.
- **Request rate:** Requests per second. Track trends for capacity planning.
- **Saturation:** CPU, memory, disk, network, connection pool usage. Know when you're about to hit a limit.

## 14. Back-of-Envelope Estimation

**Reference numbers to memorize:**
- Memory read: ~100ns
- SSD read: ~100µs
- Disk seek: ~10ms
- Network round trip (same datacenter): ~500µs
- Network round trip (cross-continent): ~100ms
- HTTP request (light): ~10ms server time
- LLM inference (7B, single query): ~100ms-1s on GPU
- Vector search (1M vectors, brute force): ~10ms
- Vector search (1M vectors, ANN index): ~1ms

## 15. AI-Specific Patterns

**LLM caching:** Cache LLM responses for exact query matches. Most effective for high-volume simple queries (classification, extraction). Semantic caching (cache on embedding similarity instead of exact match) is the next frontier.

**Embedding cache:** Cache document embeddings so you only compute them once. FAISS index is essentially an embedding cache with search capability.

**Vector DB sharding:** Shard by document collection, tenant, or language. Keeps each shard small and search fast.

**Cost optimization patterns:**
- Cascade: Try small/cheap model first; escalate to large/expensive model only when confidence is low.
- Cache frequent queries.
- Batch inference for non-real-time use.
- Use local Ollama for dev/test instead of paid API calls.

## Interview Must-Knows

- Vertical vs horizontal scaling.
- Load balancer layer 4 vs layer 7.
- Cache-aside vs write-through vs write-behind.
- SQL vs NoSQL tradeoffs.
- CAP theorem: can't have all three during partition. CP vs AP choice.
- When to use message queues.
- Rate limiting algorithms: token bucket (allows bursts) vs leaky bucket (smooth output).
- Circuit breaker pattern.
- Consistent hashing: why it's better than simple modulo for distributed caches.
- Observability: logging vs metrics vs tracing. What each is good for.
- Back-of-envelope: know approximate latencies for memory, disk, network, LLM inference.
- Cascade pattern: start cheap, escalate to expensive only when needed.
