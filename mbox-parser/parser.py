#! /usr/bin/env python3
# ~*~ utf-8 ~*~

# This code reuses the benwattsjones implementation:
# https://gist.github.com/benwattsjones/060ad83efd2b3afc8b229d41f9b246c4

import mailbox
import bs4
import argparse


def get_html_text(html):
    try:
        return bs4.BeautifulSoup(html, 'lxml').body.get_text(' ', strip=True)
    except AttributeError:  # message contents empty
        return None


class GmailMboxMessage():
    def __init__(self, email_data, outputFile):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError('Variable must be type mailbox.mboxMessage')
        self.email_data = email_data
        self.outputFile = outputFile

    def parse_email(self):
        email_labels = self.email_data['X-Gmail-Labels']
        email_date = self.email_data['Date']
        email_from = self.email_data['From']
        email_to = self.email_data['To']
        email_subject = self.email_data['Subject']
        email_text = self.read_email_payload()

    def read_email_payload(self):
        email_payload = self.email_data.get_payload()
        if self.email_data.is_multipart():
            email_messages = list(self._get_email_messages(email_payload))
        else:
            email_messages = [email_payload]
        return [self._read_email_text(msg) for msg in email_messages]

    def _get_email_messages(self, email_payload):
        for msg in email_payload:
            if isinstance(msg, (list, tuple)):
                for submsg in self._get_email_messages(msg):
                    yield submsg
            elif msg.is_multipart():
                for submsg in self._get_email_messages(msg.get_payload()):
                    yield submsg
            else:
                yield msg

    def _read_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get(
            'Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type and 'base64' not in encoding:
            msg_text = msg.get_payload()
        elif 'text/html' in content_type and 'base64' not in encoding:
            msg_text = get_html_text(msg.get_payload())
        elif content_type == 'NA':
            msg_text = get_html_text(msg)
        else:
            msg_text = None

        if msg_text:
            self.outputFile.write(msg_text)
        return (content_type, encoding, msg_text)

    def store_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get(
            'Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type and 'base64' not in encoding:
            msg_text = msg.get_payload()
        elif 'text/html' in content_type and 'base64' not in encoding:
            msg_text = get_html_text(msg.get_payload())
        elif content_type == 'NA':
            msg_text = get_html_text(msg)
        else:
            msg_text = None
        return (content_type, encoding, msg_text)

# End of library, example of use below


def main(input, output, limit):
    mbox_obj = mailbox.mbox(input)

    num_entries = len(mbox_obj)

    outputFile = open(output, 'w')

    for idx, email_obj in enumerate(mbox_obj):
        email_data = GmailMboxMessage(email_obj, outputFile)
        email_data.parse_email()

        if limit is not None:
            if idx >= limit:
                break

        print('Parsing email {0} of {1}'.format(idx, num_entries))

    outputFile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs=1, type=str,
                        help="Input file")

    parser.add_argument("-o", nargs=1, default="output.txt", type=str,
                        help="Output file (default: output.txt).")
    parser.add_argument("-l", nargs=1, default=None, type=int,
                        help="Max number of items (default: None -- No limits).")

    args = parser.parse_args()
    input = args.filename[0]

    output = args.o
    if isinstance(output, list):
        output = output[0]

    limit = args.l
    if isinstance(limit, list):
        limit = limit[0]

    main(input, output, limit)
