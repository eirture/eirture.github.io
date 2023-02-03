#!/usr/bin/env python3
import datetime
import os
import subprocess
import sys

TABLE_ANCHOR = '## Blogs\n'

TABLE_HEADER = '''
| Date | Title |
| ---- | ----- |
'''

TABLE_ROW_TEMPLATE = '| {date:%Y-%m-%d} | [{title}]({path}) |\n'

READ_MAX_LINES = 8
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

POSTS_DIR = 'source/_posts'
README_PATH = 'README.md'

ignore_files = [
    '.DS_Store'
]


def get_updated(path: str):
    '''get updated datetime from git log'''
    cmd = 'git log -n 1 --pretty=format:"%ad" --date=format:"{}" -- {}'.format(
        DATE_FORMAT,
        path
    )

    p = subprocess.Popen(
        cmd,
        cwd=os.getcwd(),
        shell=True,
        stdout=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return ''
    return stdout.decode('utf-8')


def parse_meta(path):
    '''parse meta from post header'''
    meta = {}
    with open(path, 'rb') as f:
        started = False
        for i in range(READ_MAX_LINES):
            line = f.readline().strip()
            if line == b'---':
                if started:
                    return meta
                else:
                    started = True
                    continue
            else:
                parts = line.decode('utf-8').split(': ', 1)
                if len(parts) != 2:
                    continue
                key = parts[0]
                v = {
                    'date': lambda v: datetime.datetime.strptime(v, DATE_FORMAT)
                }.get(key, lambda v: v)(parts[1])
                meta[key] = v
    return meta


def parse_date(ds: str):
    return datetime.datetime.strptime(ds, DATE_FORMAT)


def scan_metas():
    post_metas = []
    for post in os.listdir(POSTS_DIR):
        if post in ignore_files:
            continue
        fullpath = os.path.join(POSTS_DIR, post)
        meta = parse_meta(fullpath)
        # if 'updated' not in meta:
        #     meta['updated'] = get_updated(fullpath)
        meta['path'] = fullpath
        post_metas.append(meta)

    return post_metas


def update_readme(metas):
    table_rows = []
    for meta in sorted(metas, key=lambda m: m['date'], reverse=True):
        row = TABLE_ROW_TEMPLATE.format(**meta)
        table_rows.append(row)

    with open(README_PATH, 'r+') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line == TABLE_ANCHOR:
                f.seek(0, 0)
                f.writelines(lines[:i+1])
                f.write(TABLE_HEADER)
                f.writelines(table_rows)
        f.truncate()


def main():
    metas = scan_metas()
    update_readme(metas)


if __name__ == '__main__':
    main()
