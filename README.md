# mail2csv

This command-line utility converts the contents of a `Maildir` to a CSV file. Each header becomes a CSV column, and each email becomes a row.

```
$ mail2csv example/
Date,Subject,From
"Wed, 16 May 2018 20:05:16 +0000",An email,Bob <bob@example.com>
"Wed, 16 May 2018 20:07:52 +0000",Also an email,Alice <alice@example.com>
```

By default, only `Date`, `Subject` and `From` headers are shown. Use `--headers` to specify which other headers to include, and `--all-headers` to include them all.

## Requirements

- Python 2 or 3.

## Installation

```
cp mail2csv.py /usr/local/bin/mail2csv
```

## Full usage

```
usage: mail2csv.py [-h] [--outfile OUTFILE] [--headers HEADERS [HEADERS ...]]
                   [--all-headers]
                   maildir

Convert maildir to CSV.

positional arguments:
  maildir               Directory to read from

optional arguments:
  -h, --help            show this help message and exit
  --outfile OUTFILE     File to output to. Standard output is used if this is
                        not specified
  --headers HEADERS [HEADERS ...]
                        Headers to include
  --all-headers         Include all headers. Alias for --headers '*'
```
