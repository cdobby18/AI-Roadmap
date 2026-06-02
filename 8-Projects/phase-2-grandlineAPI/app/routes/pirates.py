# ─── app/routes/pirates.py ────────────────────────────────────────────────────
# CRUD endpoints for Pirates.
# Public:   GET /pirates, GET /pirates/{id}
# Protected: POST, PUT, DELETE (require valid JWT — marines only)
#
# TODO: Import APIRouter, HTTPException, status, Depends, BackgroundTasks from fastapi
#       Import Session from sqlalchemy.orm
#       Import get_db from app.database
#       Import Pirate from app.models
#       Import PirateCreate, PirateUpdate, PirateResponse from app.schemas.pirate
#       Import get_current_marine from app.auth.jwt_bearer
#
# TODO: Create the router:  router = APIRouter()
#
# ─── GET /pirates ─────────────────────────────────────────────────────────────
# TODO: Return a list of all pirates from the database
#       Hint: db.query(Pirate).all()
#       Response model: list[PirateResponse]
#
# ─── GET /pirates/{pirate_id} ─────────────────────────────────────────────────
# TODO: Return a single pirate by ID
#       Hint: db.query(Pirate).filter(Pirate.id == pirate_id).first()
#       If not found → raise HTTPException 404 "Pirate not found"
#       Response model: PirateResponse
#
# ─── POST /pirates ────────────────────────────────────────────────────────────
# TODO: Create a new pirate record (protected)
#       Steps:
#         1. Create a Pirate ORM object from the request data (pirate_data.model_dump())
#         2. db.add(pirate), db.commit(), db.refresh(pirate)
#         3. Return the created pirate
#       Response model: PirateResponse, status_code=201
#
# ─── PUT /pirates/{pirate_id} ─────────────────────────────────────────────────
# TODO: Update an existing pirate (protected)
#       Steps:
#         1. Fetch the existing pirate (404 if not found)
#         2. Loop through pirate_data.model_dump(exclude_unset=True).items()
#            and setattr(pirate, key, value) for each
#            (exclude_unset=True means only update fields the client actually sent)
#         3. db.commit(), db.refresh(pirate)
#         4. Return the updated pirate
#
# ─── DELETE /pirates/{pirate_id} ──────────────────────────────────────────────
# TODO: Delete a pirate (protected)
#       Steps:
#         1. Fetch the pirate (404 if not found)
#         2. db.delete(pirate), db.commit()
#         3. Return 204 No Content (no body needed)
#
# ─── BACKGROUND TASK: recalculate_bounty ──────────────────────────────────────
# TODO: Write a regular function recalculate_bounty(pirate_id: int, db: Session)
#       This simulates a slow bounty update that runs AFTER the response is sent.
#       Steps (keep it simple):
#         1. Fetch the pirate from DB
#         2. Multiply the bounty by a small factor (e.g. 1.1 — 10% increase)
#         3. Commit the change
#         4. Print/log "Bounty updated for pirate {pirate_id}"
#
# TODO: Wire it up — in POST /pirates, add a background_tasks parameter
#       and call background_tasks.add_task(recalculate_bounty, pirate.id, db)
#       The client gets the 201 response immediately; the bounty update runs after.
