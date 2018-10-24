from operator import itemgetter


def Filter(**kargs):
    def filt(data, sr, sctx, sccol, matches):
        typed = data['context']['typed']
        # When query is empty, sort candidates by their last_updated field
        # in descending order so that recently updated items are first in the
        # list
        if typed == 'JI':
            res = sorted(matches, key=itemgetter('last_updated'), reverse=True)
            return res
        return matches
    return filt

