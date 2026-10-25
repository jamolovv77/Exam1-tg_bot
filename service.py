from connection import connection_db


async def add_envent_db(title: str, capacity: int, event_date: str):
    conn = await connection_db()
    try:
        await conn.execute(
            "insert into events (title,capacity,event_date) VALUES (1$, 2$, 3$)",
            title,capacity,event_date 
            
        )
    finally:
        await conn.close()



async def get_all_events_db():
    conn = await connection_db()
    try:
        rows = await conn.fetch("select id, title, capacity, event_date FROM order by id")
        return rows
    finally:
        await conn.close()
async def get_event_db(event_id: int):
    conn = await connection_db()
    try:
        row = await conn.fetchrow("SELECT id, title, cpacity, event_date from events where id = $1", event_id)
        return row
    finally:
        await conn.close()
async def get_user_registration_db(user_id: str, event_id: int):
    conn = await connection_db()
    try:
        row = await conn.fetchrow(
            "SELSECT id, status from registrations where user_id = $1 and event_id = $2",
            str(user_id), event_id
        )
        return row
    finally:
        await conn.close()
async def register_user_db(user_id: str, event_id: int):
    conn = await connection_db()

    try:
        event = await get_event_db(event_id)
        if not event:
            return "not_found"
            
        capacity = event["capacity"]
        confirmed_count = await get_confirmed_count_db(event_id)
        
        status = "confirmed" if confirmed_count < capacity else "waitlist"
        
        await conn.execute(
            "INSERT INTO registrations (user_id, event_id, status) VALUES ($1, $2, $3)",
            str(user_id), event_id, status
        )
        return status
    finally:
        await conn.close()
async def cancel_registration_db(user_id: str, event_id: int):

    conn = await connection_db()
    try:
        reg = await get_user_registration_db(user_id, event_id)

        reg_id, old_status = reg["id"], reg["status"]

        await conn.execute("DELETE FROM registrations WHERE id = $1", reg_id)

        if old_status == "confirmed":
            waitlist_user = await conn.fetchrow(
                "SELECT id, user_id FROM registrations WHERE event_id = $1 AND status = 'waitlist' ORDER BY registered_at ASC LIMIT 1",event_id
            )
            if waitlist_user:
                waitlist_reg_id = waitlist_user["id"]
                promoted_user_id = waitlist_user["user_id"]


                await conn.execute("UPDATE registrations set status = 'confirmed' where id = $1",waitlist_reg_id)

            return old_status,promoted_user_id
    finally:
        await conn.close()





async def get_user_events_db(user_id: str):
    conn = await connection_db()
    try:
        rows = await conn.fetch("""
select e.title, e.event_date, r.status, e.id
from registrations r
join events e on r. event_id = e.id
where r.user_id = $1





""",
str(user_id)
)
        return rows
    finally:
        await conn.close()