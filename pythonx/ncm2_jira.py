# -*- coding: utf-8 -*-

import vim
from ncm2 import Ncm2Source, getLogger

from jira_rt_completion_server.jira_completer import (
    load_lines,
    get_jira_candidates
)
from datetime import datetime

logger = getLogger(__name__)


def log(msg):
    now = str(datetime.now())
    with open('/tmp/ncm2-jira.log', 'a') as file_:
        file_.write('%s %s\n' % (now, msg))


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
