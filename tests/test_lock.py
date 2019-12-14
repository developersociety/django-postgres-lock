from django.db import connection
from django.test import TransactionTestCase

from postgres_lock.lock import PostgresLock


class PostgresLockTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        cursor = connection.cursor()

        cursor.execute(
            "SELECT oid FROM pg_database WHERE datname=%(datname)s",
            {"datname": connection.settings_dict["NAME"]},
        )
        cls.db_oid = cursor.fetchone()[0]

        cursor.close()

    def assertNumLocks(self, expected):
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM pg_locks WHERE database=%(database)s AND locktype=%(locktype)s",
            {"database": self.db_oid, "locktype": "advisory"},
        )
        actual = cursor.fetchone()[0]
        cursor.close()

        self.assertEqual(actual, expected)

    def test_default_lock_id(self):
        lock = PostgresLock()

        self.assertEqual(lock.lock_id, 3814588639)

    def test_custom_lock_id(self):
        lock = PostgresLock()

        lock_id = lock.get_lock_id(name="advisory_lock")

        self.assertEqual(lock_id, 1201105184)

    def test_other_database(self):
        lock = PostgresLock(name="readonly")

        self.assertEqual(lock.lock_id, 1012845560)

    def test_standard_lock(self):
        self.assertNumLocks(0)

        lock = PostgresLock()

        self.assertEqual(lock.lock_function, "pg_advisory_lock")
        self.assertEqual(lock.unlock_function, "pg_advisory_unlock")

        with lock as acquired:
            self.assertTrue(acquired)
            self.assertNumLocks(1)

        self.assertNumLocks(0)

    def test_try_lock(self):
        self.assertNumLocks(0)

        lock = PostgresLock(try_=True)

        self.assertEqual(lock.lock_function, "pg_try_advisory_lock")
        self.assertEqual(lock.unlock_function, "pg_advisory_unlock")

        with lock as acquired:
            self.assertTrue(acquired)
            self.assertNumLocks(1)

        self.assertNumLocks(0)

    def test_shared_lock(self):
        self.assertNumLocks(0)

        lock = PostgresLock(shared=True)

        self.assertEqual(lock.lock_function, "pg_advisory_lock_shared")
        self.assertEqual(lock.unlock_function, "pg_advisory_unlock_shared")

        with lock as acquired:
            self.assertTrue(acquired)
            self.assertNumLocks(1)

        self.assertNumLocks(0)
