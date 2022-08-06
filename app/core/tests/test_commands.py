"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from django.core.management.base import CommandError


# Django commands that don't require interaction with models
@patch('core.management.commands.wait_for_db.Command.check')
class DjangoSetUpCommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2OpError] \
            * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])


class DjangoModificationCommandTests(SimpleTestCase):

    def test_upgrade_user_command_failure(self):
        with self.assertRaises(CommandError):
            call_command('upgrade_user testNotExist@example.com')

    # def test_upgrade_user_command_success(self):
