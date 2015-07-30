from token import sentences
import codecs

def give_features(hform, hlemma, hpos, dform, dlemma, dpos, bpos):

    # generator that yields features based on the following information:

    # 1 = hform
    # 2 = hpos
    # 3 = dform
    # 4 = dpos
    # 5 = bpos
    # 6 = hlemma
    # 7 = dlemma

    yield "1:%s" % hform
    yield "2:%s" % hpos
    yield "3:%s" % dform,
    yield "4:%s" % dpos
    yield "6:%s" % hlemma
    yield "7:%s" % dlemma
    yield "5:%s" % bpos

    yield "1,4:%s,%s" % (hform, dpos)
    yield "2,3:%s,%s" % (hpos, dform)
    yield "1,2:%s,%s" % (hform, hpos)
    yield "3,4:%s,%s" % (dform, dpos)
    yield "1,3:%s,%s" % (hform, dform)
    yield "2,4:%s,%s" % (hpos, dpos)
    yield "6,4:%s,%s" % (hlemma, dpos)
    yield "2,7:%s,%s" % (hpos, dlemma)
    yield "6,2:%s,%s" % (hlemma, hpos)
    yield "7,4:%s,%s" % (dlemma, dpos)
    yield "6,7:%s,%s" % (hlemma, dlemma)

    yield "1,2,3,4:%s,%s,%s,%s" % (hform, hpos, dform, dpos)
    yield "2,3,4:%s,%s,%s" % (hpos, dform, dpos)
    yield "1,3,4:%s,%s,%s" % (hform, dform, dpos)
    yield "1,2,3:%s,%s,%s" % (hform, hpos, dform)
    yield "1,2,4:%s,%s,%s" % (hform, hpos, dpos)
    yield "2,5,4:%s,%s,%s" % (hpos, bpos, dpos)
    yield "2,5,3:%s,%s,%s" % (hpos, bpos, dform)
    yield "1,5,4:%s,%s,%s" % (hform, bpos, dpos)
    yield "1,5,3:%s,%s,%s" % (hform, bpos, dform)

    yield "6,2,7,4:%s,%s,%s,%s" % (hlemma, hpos, dlemma, dpos)
    yield "2,7,4:%s,%s,%s" % (hpos, dlemma, dpos)
    yield "6,7,4:%s,%s,%s" % (hlemma, dlemma, dpos)
    yield "6,2,7:%s,%s,%s" % (hlemma, hpos, dlemma)
    yield "6,2,4:%s,%s,%s" % (hlemma, hpos, dpos)
    yield "2,5,7:%s,%s,%s" % (hpos, bpos, dlemma)
    yield "6,5,4:%s,%s,%s" % (hlemma, bpos, dpos)
    yield "6,5,7:%s,%s,%s" % (hlemma, bpos, dlemma)


def fm(infile):
    # takes a file in conll09 format, returns a feature map
    feat_map = {}  # featmap as dictionary {feature:index}
    index = 0  # index in featmap
    for sentence in sentences(codecs.open(infile, encoding='utf-8')):
        for token1 in sentence:

            # add root features
            for feature in give_features("__ROOT__", "__ROOT__", "__ROOT__", token1.form, token1.lemma, token1.pos, token1.rel):
                if feature not in feat_map:
                    feat_map[feature] = index
                    index += 1

            # add other features
            for token2 in sentence:
                for feature in give_features(token1.form, token1.lemma, token1.pos, token2.form, token2.lemma, token2.pos, token2.rel):
                    if feature not in feat_map:
                        feat_map[feature] = index
                        index += 1

    return feat_map
