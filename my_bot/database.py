#type: ignore
import psycopg
import asyncio


class Database:

    def __init__(self, config):
        self.config = config
        self.connection = None

    async def connect(self):
        self.connection = await psycopg.AsyncConnection.connect(**self.config)

    async def disconnect(self):
        await self.connection.close()

    async def execute(self, query, *params):
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, params)
            await self.connection.commit()

    async def fetchone(self, query, *params):
            async with self.connection.cursor() as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchone()

    async def fetchall(self, query, *params):
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()

    async def create_tables(self):
        await self.execute("""
        CREATE TABLE IF NOT EXISTS TelegramUsers (
            id SERIAL PRIMARY KEY,
            phone_number VARCHAR(25),
            username VARCHAR(25),
            firstname VARCHAR(25),
            adress VARCHAR(255)
        );
        """)

        await self.execute("""
        CREATE TABLE IF NOT EXISTS Mailing (
            id SERIAL PRIMARY KEY,
            username_tg INTEGER REFERENCES TelegramUsers(id),
            date_send VARCHAR(15),
            error_text VARCHAR(255)
        );
        """)

    async def add_user(self, phone_number, username, firstname, adress):
        await self.execute("INSERT INTO TelegramUsers (phone_number, username, firstname, adress)\
            VALUES (%s, %s, %s, %s) RETURNING id;", phone_number, username, firstname, adress)

    async def add_mailing(self, username_tg, date_send, error_text):
        await self.execute("INSERT INTO Mailing (username_tg, date_send, error_text)\
            VALUES (%s, %s, %s, %s);", username_tg, date_send, error_text)

    async def get_users(self):
        return await self.fetchall("SELECT id, phone_number, username, firstname, adress FROM TelegramUsers;")

    async def get_user_by_id(self, user_id):
        return await self.fetchone("SELECT * FROM TelegramUsers WHERE id = %s;", user_id)

    async def get_user_by_username(self, username):
        return await self.fetchone("SELECT * FROM TelegramUsers WHERE username = %s;", username)

    async def get_mailings(self):
        return await self.fetchall("SELECT id, username_tg, date_send, error_text FROM Mailing;")
