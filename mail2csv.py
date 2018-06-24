#!/usr/bin/env python
from __future__ import print_function

import argparse
import mailbox
import csv
import email
import re
import fnmatch
import sys

class Maildir2Csv:
    def print_err(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @staticmethod
    def run(maildir_path, outp_file, header_globs):
        # Validate
        maildir = mailbox.Maildir(maildir_path, create=False)
        keys = maildir.keys()
        if len(keys) == 0:
            # No emails = no output
            return
        # Convert each message to a dictionary
        messages = []
        all_headers_set = set([])
        for key in keys:
            email_txt = str(maildir[key])
            msg = email.message_from_string(email_txt)
            msg_dict = {}
            for header_name, header_value in msg.items():
                numbered_header_name = header_name
                header_number = 1
                while numbered_header_name in msg_dict:
                    header_number = header_number + 1
                    numbered_header_name = "{}-{}".format(header_name, header_number)
                msg_dict[numbered_header_name] = header_value
                all_headers_set.add(numbered_header_name)
            messages.append(msg_dict)
        all_headers = sorted(all_headers_set)
        # Determine which headers to use: Treat requested header names as globs against all now headers
        use_headers_set = set([])
        use_headers = []
        for header_glob in header_globs:
            header_pattern = re.compile(fnmatch.translate(header_glob))
            matches = 0
            for header_name in all_headers:
                if header_pattern.match(header_name) and not header_name in use_headers_set:
                    # Track list (in order of matches) with no duplicates
                    use_headers_set.add(header_name)
                    use_headers.append(header_name)
                    matches = matches + 1
            if matches == 0 and '*' not in header_glob:
                # Usually triggers if a typo has occurred
                Maildir2Csv.print_err('WARNING: Header \'{}\' does not appear in any email messages, and will not be included in the output'.format(header_glob))
        # Write out to CSV
        dw = csv.DictWriter(outp_file, fieldnames=use_headers, extrasaction='ignore')
        dw.writeheader()
        dw.writerows(messages)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert maildir to CSV.')
    parser.add_argument('--outfile',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="File to output to. Standard output is used if this is not specified")
    parser.add_argument('--maildir',
                        help="Directory to read from",
                        default="mail/")
    parser.add_argument('--headers',
                        help="Headers to include",
                        default=['Date', 'Subject', 'From'],
                        nargs='+')
    parser.add_argument('--all-headers',
                        help="Include all headers. Alias for --headers '*'",
                        action='store_true')
    args = parser.parse_args()
    if args.all_headers:
        header_globs = ['*']
    else:
        header_globs = args.headers
    Maildir2Csv.run(args.maildir, args.outfile, header_globs)
