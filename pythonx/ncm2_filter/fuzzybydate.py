from operator import itemgetter
from datetime import datetime

def log(msg):
    now = str(datetime.now())
    with open('/tmp/ncm2-jira.log', 'a') as file_:
        file_.write('%s %s\n' % (now, msg))


def Filter(**kargs):
    def filt(data, sr, sctx, sccol, matches):
        typed = data['context']['typed']
        # When query is empty, sort candidates by their last_updated field
        # in descending order so that recently updated items are first in the
        # list
        #log('FILTER TYPED: %s' % typed)
        if typed.endswith('JI'):
            res = sorted(matches, key=itemgetter('last_updated'), reverse=True)
            return res
        return matches
    return filt

