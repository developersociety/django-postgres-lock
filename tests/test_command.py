from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class TestCommandLockCommand(TestCase):
    def test_command(self):
        result = call_command("command_lock", "--", "true")

        self.assertIsNone(result)

    def test_failed_command(self):
        with self.assertRaises(SystemExit) as cm:
            call_command("command_lock", "--", "false")

            self.assertEqual(cm.exception.code, 1)

    @mock.patch("postgres_lock.lock.PostgresLock.__exit__")
    @mock.patch("postgres_lock.lock.PostgresLock.__enter__")
    def test_lock_failed(self, mock_enter, mock_exit):
        mock_enter.return_value = False
        mock_exit.return_value = None

        with self.assertRaisesMessage(CommandError, "Unable to acquire lock"):
            call_command("command_lock", "--", "true")
