import sys


def log(msg):
    from datetime import datetime

    now = str(datetime.now())
    with open('/tmp/ncm2-jira.log', 'a') as file_:
        file_.write('%s %s\n' % (now, msg))


def Sorter(**kargs):
    def key(e):
        w = e['word']
        ud = e['user_data']
        hl = ud['match_highlight']

        # prefer less pieces
        pieces = len(hl)

        # prefer earlier match
        first_match = sys.maxsize
        if len(hl):
            first_match = hl[0][0]

        # prefer shorter span
        span = sys.maxsize
        if len(hl):
            span = hl[-1][1] - hl[0][0]

        # alphanum
        scw = w.swapcase()

        return [pieces, first_match, span, scw]

    def sort(matches: list):
        # log('matches: %s' % matches)
        # raise RuntimeError('CUSTOM SORTER: %s' % matches)
        matches.sort(key=key)
        return matches

    return sort
