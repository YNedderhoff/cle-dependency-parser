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

    yield "1:{0}".format(hform)
    yield "2:{0}".format(hpos)
    yield "3:{0}".format(dform)
    yield "4:{0}".format(dpos)
    yield "6:{0}".format(hlemma)
    yield "7:{0}".format(dlemma)
    yield "5:{0}".format(bpos)

    yield "1,4:{0},{1}".format(hform, dpos)
    yield "2,3:{0},{1}".format(hpos, dform)
    yield "1,2:{0},{1}".format(hform, hpos)
    yield "3,4:{0},{1}".format(dform, dpos)
    yield "1,3:{0},{1}".format(hform, dform)
    yield "2,4:{0},{1}".format(hpos, dpos)
    yield "6,4:{0},{1}".format(hlemma, dpos)
    yield "2,7:{0},{1}".format(hpos, dlemma)
    yield "6,2:{0},{1}".format(hlemma, hpos)
    yield "7,4:{0},{1}".format(dlemma, dpos)
    yield "6,7:{0},{1}".format(hlemma, dlemma)

    yield "1,2,3,4:{0},{1},{2},{3}".format(hform, hpos, dform, dpos)
    yield "2,3,4:{0},{1},{2}".format(hpos, dform, dpos)
    yield "1,3,4:{0},{1},{2}".format(hform, dform, dpos)
    yield "1,2,3:{0},{1},{2}".format(hform, hpos, dform)
    yield "1,2,4:{0},{1},{2}".format(hform, hpos, dpos)
    yield "2,5,4:{0},{1},{2}".format(hpos, bpos, dpos)
    yield "2,5,3:{0},{1},{2}".format(hpos, bpos, dform)
    yield "1,5,4:{0},{1},{2}".format(hform, bpos, dpos)
    yield "1,5,3:{0},{1},{2}".format(hform, bpos, dform)

    yield "6,2,7,4:{0},{1},{2},{3}".format(hlemma, hpos, dlemma, dpos)
    yield "2,7,4:{0},{1},{2}".format(hpos, dlemma, dpos)
    yield "6,7,4:{0},{1},{2}".format(hlemma, dlemma, dpos)
    yield "6,2,7:{0},{1},{2}".format(hlemma, hpos, dlemma)
    yield "6,2,4:{0},{1},{2}".format(hlemma, hpos, dpos)
    yield "2,5,7:{0},{1},{2}".format(hpos, bpos, dlemma)
    yield "6,5,4:{0},{1},{2}".format(hlemma, bpos, dpos)
    yield "6,5,7:{0},{1},{2}".format(hlemma, bpos, dlemma)


def fm(infile):
    # takes a file in conll06 format, returns a feature map
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
