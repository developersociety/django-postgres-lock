from zlib import crc32

from django.db import DEFAULT_DB_ALIAS, connections


class PostgresLock:
    def __init__(self, name=None, try_=False, shared=False, using=DEFAULT_DB_ALIAS):
        # If a name isn't provided then we use the name of the database connection by default.
        # This means that the entire Django app will be using a single lock - which is probably
        # something to avoid, but is available if needed.
        if name is None:
            name = using

        self.lock_id = self.get_lock_id(name=name)
        self.try_lock = try_
        self.shared_lock = shared
        self.database_connection = connections[using]

        if try_:
            try_str = "_try"
        else:
            try_str = ""

        if shared:
            shared_str = "_shared"
        else:
            shared_str = ""

        self.lock_function = f"pg{try_str}_advisory_lock{shared_str}"
        self.unlock_function = f"pg_advisory_unlock{shared_str}"

    def get_lock_id(self, name):
        """
        Generate an integer suitable for Postgres advisory locks.
        """
        # Python 3 crc32 returns an unsigned integer, so we need to ensure we return a signed
        # integer instead.
        return crc32(name.encode()) & 0xFFFFFFFF

    def lock(self):
        self.cursor = self.database_connection.cursor()
        self.cursor.execute(
            f"SELECT {self.lock_function}(%(lock_id)s)",
            {"lock_id": self.lock_id},
        )

        if self.try_lock:
            result = self.cursor.fetchone()[0]
        else:
            result = True

        return result

    def release(self):
        self.cursor.execute(
            f"SELECT {self.unlock_function}(%(lock_id)s)",
            {"lock_id": self.lock_id},
        )
        self.cursor.close()

    def __enter__(self):
        return self.lock()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
