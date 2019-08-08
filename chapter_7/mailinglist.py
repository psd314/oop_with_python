from collections import defaultdict
from send_email import send_email


class MailingList:
    def __init__(self, data_file):
        self.data_file = data_file
        self.email_map = defaultdict(set)

    def add_to_group(self, email, group):
        self.email_map[email].add(group)

    def emails_in_group(self, *groups):
        groups = set(groups)
        emails = set()
        for e, g in self.email_map.items():
            if g & groups:
                emails.add(e)
        return emails

    def send_mailing(self, subject, message, from_addr, *groups, headers=None):
        emails = self.emails_in_group(*groups)
        send_email(subject, message, from_addr, *emails, headers=headers)

    def save(self):
        with open(self.data_file, 'w') as file:
            for email, groups in self.email_map.items():
                file.write(
                    '{} {}\n'.format(email, ','.join(groups))
                )

    def load(self):
        self.email_map = defaultdict(set)
        try:
            with open(self.data_file) as file:
                for line in file:
                    email, groups = line.strip().split(' ')
                    groups = set(groups.split(','))
                    self.email_map[email] = groups
        except IOError:
            pass

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
