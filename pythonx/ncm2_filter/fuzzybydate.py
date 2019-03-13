from ncm2_filter.abbr_ellipsis import Filter as EllipsisFilter

from datetime import datetime
from operator import itemgetter


def log(msg):
    now = str(datetime.now())
    with open('/tmp/ncm2-jira.log', 'a') as file_:
        file_.write('%s %s\n' % (now, msg))


ellipses_filter = EllipsisFilter(limit=120, ellipsis='…')


def Filter(**kargs):
    def filt(data, sr, sctx, sccol, matches):
        typed = data['context']['typed']
        # When query is empty, sort candidates by their last_updated field
        # in descending order so that recently updated items are first in the
        # list
        #log('FILTER TYPED: %s' % typed)
        result = matches
        if typed.endswith('JI'):
            result = sorted(matches, key=itemgetter('last_updated'), reverse=True)
        return ellipses_filter(data, sr, sctx, sccol, result)
    return filt
