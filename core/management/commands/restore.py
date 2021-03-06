"""  __      __    __               ___
    /  \    /  \__|  | _ __        /   \
    \   \/\/   /  |  |/ /  |  __  |  |  |
     \        /|  |    <|  | |__| |  |  |
      \__/\__/ |__|__|__\__|       \___/

A web service for sharing opinions and avoiding arguments

@file       core/management/restore.py
@copyright  GNU Public License, 2018
@authors    Frank Imeson
@brief      A managment script for restoring the database
"""


# *******************************************************************************
# Imports
# *******************************************************************************
import os
import re
import glob
import datetime
import psycopg2

from django.core.management.base import BaseCommand


# *******************************************************************************
# Defines
# *******************************************************************************


# *******************************************************************************
# Methods
# *******************************************************************************


class Command(BaseCommand):
    """Restores an archived database."""
    help = __doc__

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('archive_path', nargs='?', type=str)

        # Named (optional) arguments
        parser.add_argument(
            '--site',
            choices=['local', 'wiki-o', 'wiki-x'],
            default='wiki-o',
            help='Choose which site the archive must come from.',
        )

        parser.add_argument(
            '--do_not_delete',
            action='store_true',
            help='Do not delete the existing database.',
        )

        parser.add_argument(
            '--backup_dir',
            default='/home/django/backups/database',
            help='The directory that is searched for archive files.',
        )

    def handle(self, *args, **options):
        """The method that is run when the commandline is invoked."""

        # Check that postgress username/password is setup.
        if not os.environ.get('PGUSER') or not os.environ.get('PGPASSWORD'):
            s = "Error: PGUSER and or PGPASSWORD environment variable does not exist!\n"
            s += "       Please populate the username and password for postgresql."
            print(s)
            return

        # Pick the latest archive.
        archive_path = options['archive_path']
        if archive_path is None:
            latest_date = None
            glob_string = options['backup_dir'] + '/* - feedback.%s.sql.gz' % options['site']
            for archive in glob.glob(glob_string):
                date = re.search(r'\d{4}\.\d{2}\.\d{2}', archive)
                if date is None:
                    continue
                date = date.group()
                date = datetime.datetime.strptime(date, '%Y.%m.%d')
                print(date, archive)
                if latest_date is None or date > latest_date:
                    latest_date = date
                    archive_path = archive

        # Update the database.
        user = os.environ.get('PGUSER')
        password = os.environ.get('PGPASSWORD')
        with psycopg2.connect(host="localhost", database="postgres",
                              user=user, password=password) as conn:
            with conn.cursor() as cur:
                conn.autocommit = True
                # Break all connections to the database.
                pg_cmd = "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity"
                pg_cmd += " WHERE pg_stat_activity.datname = 'feedback_wiki_o' AND"
                pg_cmd += " pid <> pg_backend_pid();"
                cur.execute(pg_cmd)
                # Deltete
                if not options['do_not_delete']:
                    cur.execute("DROP DATABASE IF EXISTS feedback_wiki_o;")
                    print('Deleted old database.')
                # Create
                cur.execute("CREATE DATABASE feedback_wiki_o;")
                # Restore (large archives should not be loaded into python).
                print("Restoring %s" % archive_path)
                cmd = 'gunzip < "%s" | ' % archive_path
                cmd += 'psql -h localhost --username=%s -d feedback_wiki_o' % user
                os.system(cmd)
                # Permissions (probably not necessary).
                cur.execute("GRANT ALL PRIVILEGES ON DATABASE feedback_wiki_o TO %s;" % user)
        print("Done")
