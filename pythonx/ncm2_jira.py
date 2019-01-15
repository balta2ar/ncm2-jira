# -*- coding: utf-8 -*-
from datetime import datetime
from operator import itemgetter
from os.path import expanduser, expandvars

import vim

from ncm2 import getLogger, Ncm2Source

logger = getLogger(__name__)


def log(msg):
    now = str(datetime.now())
    with open('/tmp/ncm2-jira.log', 'a') as file_:
        file_.write('%s %s\n' % (now, msg))


def load_lines(filename):
    # 0 - key
    # 1 - subject
    # 2 - status
    # 3 - owner
    # 4 - last updated
    filename = expanduser(expandvars(filename))
    get_subset = itemgetter(0, 1, 4)
    with open(filename) as file_:
        lines = [get_subset(line.strip().split('\t'))
                 for line in file_.readlines()]
    log('load_lines: #: %s' % len(lines))
    return lines


def get_jira_candidates(candidates, _current_prefix, matcher_key):
    max_ticket_len = max(len(ticket)
                         for ticket, _title, _last_updated in candidates)
    ticket_formatter = '%' + str(max_ticket_len) + 's'
    return [{
        'word': ticket,
        'abbr': ticket_formatter % ticket + ' ' + title,
        #matcher_key: current_prefix + title,
        matcher_key: 'JI' + title,
        'last_updated': last_updated,
    }
        for ticket, title, last_updated in candidates]


class Source(Ncm2Source):
    def __init__(self, nvim):
        super(Source, self).__init__(nvim)
        self.executable_look = nvim.call('executable', 'look')

    def on_complete(self, ctx):

        query = ctx['base']

        candidates_filename = '~/.cache/jira/jira.candidates.tsv'
        candidates = load_lines(candidates_filename)
        matches = get_jira_candidates(candidates, query, 'custom')
        self.complete(ctx, ctx['startccol'], matches)


source = Source(vim)

on_complete = source.on_complete
