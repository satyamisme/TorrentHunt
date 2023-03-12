'''API to connect to the database server'''

import asyncpg


class DataBase:
    def __init__(self, user, password, database):
        self.user = user
        self.password = password
        self.database = database

    # Query on the database
    async def query(self, method, query, *args):
        con = await asyncpg.connect(
            user=self.user,
            password=self.password,
            database=self.database,
        )
        row = await getattr(con, method)(query, *args)

        await con.close()
        return row

    # Insert user into database
    async def set_user(self, message, referrer=None):
        query = '''
        INSERT INTO USERS
            (user_id, user_type, username, first_name, last_name, referrer)
            VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (user_id)
        DO NOTHING
        '''

        # If chat type if group/channel
        if message.chat.type.name != 'PRIVATE':
            message.chat.first_name = message.chat.title
            message.chat.last_name = None

        await self.query(
            'execute',
            query,
            message.chat.id,
            message.chat.type.name,
            message.chat.username,
            message.chat.first_name,
            message.chat.last_name,
            str(referrer) if referrer else None,
        )
