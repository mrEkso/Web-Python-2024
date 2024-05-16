import psycopg
from psycopg import rows

from app.db.database import conn_pool


def get_users(skip: int = 0, limit: int = 10):
    with conn_pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM users OFFSET %s LIMIT %s", (skip, limit))
            users = cur.fetchall()
    return users


def get_user(user_id: int):
    with conn_pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()
    return user


def get_user_by_username(username: str):
    with conn_pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
    return user


def create_user(user_data):
    with conn_pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("INSERT INTO users (username, hashed_password, is_admin) VALUES (%s, %s, %s) RETURNING *",
                        (user_data.username, user_data.password, user_data.is_admin))
            user = cur.fetchone()
        conn.commit()
    return user


def update_user(user_id: int, user_data):
    with conn_pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("""
                UPDATE users
                SET username = %s, hashed_password = %s, is_admin = %s
                WHERE id = %s
                RETURNING *
            """, (user_data.username, user_data.password, user_data.is_admin, user_id))
            updated_user = cur.fetchone()
        conn.commit()
    return updated_user


def delete_user(user_id: int):
    with conn_pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (user_id,))
            user = cur.fetchone()
        conn.commit()
    return user
