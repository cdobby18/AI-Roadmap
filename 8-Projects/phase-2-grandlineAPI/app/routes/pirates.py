# ─── app/routes/pirates.py ────────────────────────────────────────────────────
# CRUD endpoints for Pirates.
# Public:    GET /pirates, GET /pirates/{id}
# Protected: POST, PUT, DELETE (require valid JWT — marines only)
#
# Data source: app/store.py  (in-memory lists — no database or ORM)
# All operations read from or mutate pirates_db directly.
#
# TODO: Import APIRouter, HTTPException, status, Depends, BackgroundTasks from fastapi
#       Import pirates_db, next_pirate_id from app.store  (the in-memory list)
#       Import PirateCreate, PirateUpdate, PirateResponse from app.schemas.pirate
#       Import get_current_marine from app.auth.jwt_bearer
#
# TODO: Create the router:  router = APIRouter()
#
# ─── GET /pirates ─────────────────────────────────────────────────────────────
# TODO: Return the full pirates_db list
#       Response model: list[PirateResponse]
#       Just return pirates_db as-is — Pydantic will validate each dict
#
# ─── GET /pirates/{pirate_id} ─────────────────────────────────────────────────
# TODO: Find and return a single pirate by ID
#       Use next(item for item in pirates_db if item["id"] == pirate_id, None)
#       OR use the helper get_pirate_by_id() from store.py if you wrote it
#       If not found → raise HTTPException 404 "Pirate not found"
#       Response model: PirateResponse
#
# ─── POST /pirates ────────────────────────────────────────────────────────────
# TODO: Create a new pirate (protected — requires JWT)
#       Steps:
#         1. Declare global next_pirate_id so you can modify it
#         2. Build a new pirate dict from pirate_data.model_dump()
#            Add "id": next_pirate_id to the dict
#         3. Append the new dict to pirates_db
#         4. Increment next_pirate_id by 1
#         5. Add the background task (see below)
#         6. Return the new pirate dict
#       Response model: PirateResponse, status_code=201
#
# ─── PUT /pirates/{pirate_id} ─────────────────────────────────────────────────
# TODO: Update an existing pirate (protected)
#       Steps:
#         1. Find the pirate dict in pirates_db (404 if not found)
#         2. Call pirate_data.model_dump(exclude_unset=True) to get only sent fields
#            (exclude_unset=True means fields the client didn't send stay unchanged)
#         3. Update the dict in-place: pirate.update(changes)
#            OR loop through items and set each key: pirate[key] = value
#         4. Return the updated pirate dict
#       Response model: PirateResponse
#
# ─── DELETE /pirates/{pirate_id} ──────────────────────────────────────────────
# TODO: Delete a pirate (protected)
#       Steps:
#         1. Find the pirate dict (404 if not found)
#         2. Remove it from pirates_db:  pirates_db.remove(pirate)
#         3. Return HTTP 204 No Content — use Response(status_code=204) or
#            raise HTTPException won't work here; use from fastapi import Response
#            and return Response(status_code=status.HTTP_204_NO_CONTENT)
#
# ─── BACKGROUND TASK: recalculate_bounty ──────────────────────────────────────
# TODO: Write a regular function recalculate_bounty(pirate_id: int)
#       This simulates a slow bounty update that runs AFTER the response is sent.
#       Steps:
#         1. Find the pirate dict in pirates_db by id
#         2. Multiply the bounty by 1.1 (10% increase)
#         3. Update the dict in-place
#         4. Print: f"Bounty updated for pirate {pirate_id}"
#       No DB commit needed — the list is already updated in memory
#
# TODO: Wire it up — in POST /pirates, add background_tasks: BackgroundTasks
#       and call background_tasks.add_task(recalculate_bounty, new_pirate["id"])
#       The client gets the 201 response immediately; the bounty update runs after
