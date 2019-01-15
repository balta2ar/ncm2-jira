# -*- coding: utf-8 -*-

import vim
from ncm2 import Ncm2Source, getLogger

# from jira_rt_completion_server.jira_completer import (
#     load_lines,
#     get_jira_candidates
# )
from datetime import datetime
import io
from operator import itemgetter

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
    # filename = expanduser(expandvars(filename))
    data = """OFFICE_IT-1257	Fix hg hook in cs/rnd-tests repo	Resolved	user1	2018-02-27
IT_SUPPORT-236	Configure certificates on https://someurl.company.net	Resolved	user2	2018-03-02
IT_DEV-319	Hypertext links to Crucible reviews in RT comments	On Hold	<NA>	2018-03-12
GENERAL-1874	Re: changes for 2018 (high level summary)	New	<NA>	2018-03-10
DEMO-56	my test	Open	user3	2018-03-06
ACCESS-6092	Please create bot user for SecretProject <-> TopSecretProject interaction	Resolved	user4	2018-03-05
ACCESS-2432	wrong permissions in test project. user1	Resolved	user1	2018-02-27"""

    get_subset = itemgetter(0, 1, 4)
    #with open(filename) as file_:
        # lines = [get_subset(line.strip().split('\t')) for line in file_.readlines()]
    # with io.StringIO(data) as file_:
    lines = [get_subset(line.strip().split('\t')) for line in data.splitlines()]
    log('load_lines: #: %s' % len(lines))
    return lines


def get_jira_candidates(candidates, current_prefix, matcher_key):
    max_ticket_len = max(len(ticket) for ticket, _title, _last_updated in candidates)
    ticket_formatter = '%' + str(max_ticket_len) + 's'
    return [{'word': ticket,
             'abbr': ticket_formatter % ticket + ' ' + title,
             matcher_key: current_prefix + title,
             'last_updated': last_updated,
             }
            # matcher_key: current_prefix + title, }
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
