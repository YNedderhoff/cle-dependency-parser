from token import sentences
import codecs


def give_features(hform, hlemma, hpos, dform, dlemma, dpos, bpos, direction, distance):

    # generator that yields features based on the following information:

    # 1 = hform
    # 2 = hpos
    # 3 = dform
    # 4 = dpos
    # 5 = bpos
    # 6 = hlemma
    # 7 = dlemma

    yield u'1,dir,dist:{0},{1},{2}'.format(hform, direction, distance)
    yield u'2,dir,dist:{0},{1},{2}'.format(hpos, direction, distance)
    yield u'3,dir,dist:{0},{1},{2}'.format(dform, direction, distance)
    yield u'4,dir,dist:{0},{1},{2}'.format(dpos, direction, distance)
    yield u'6,dir,dist:{0},{1},{2}'.format(hlemma, direction, distance)
    yield u'7,dir,dist:{0},{1},{2}'.format(dlemma, direction, distance)
    yield u'5,dir,dist:{0},{1},{2}'.format(bpos, direction, distance)

    yield u'1,4,dir,dist:{0},{1},{2},{3}'.format(hform, dpos, direction, distance)
    yield u'2,3,dir,dist:{0},{1},{2},{3}'.format(hpos, dform, direction, distance)
    yield u'1,2,dir,dist:{0},{1},{2},{3}'.format(hform, hpos, direction, distance)
    yield u'3,4,dir,dist:{0},{1},{2},{3}'.format(dform, dpos, direction, distance)
    yield u'1,3,dir,dist:{0},{1},{2},{3}'.format(hform, dform, direction, distance)
    yield u'2,4,dir,dist:{0},{1},{2},{3}'.format(hpos, dpos, direction, distance)
    yield u'6,4,dir,dist:{0},{1},{2},{3}'.format(hlemma, dpos, direction, distance)
    yield u'2,7,dir,dist:{0},{1},{2},{3}'.format(hpos, dlemma, direction, distance)
    yield u'6,2,dir,dist:{0},{1},{2},{3}'.format(hlemma, hpos, direction, distance)
    yield u'7,4,dir,dist:{0},{1},{2},{3}'.format(dlemma, dpos, direction, distance)
    yield u'6,7,dir,dist:{0},{1},{2},{3}'.format(hlemma, dlemma, direction, distance)

    yield u'1,2,3,4,dir,dist:{0},{1},{2},{3},{4},{5}'.format(hform, hpos, dform, dpos, direction, distance)
    yield u'2,3,4,dir,dist:{0},{1},{2},{3},{4}'.format(hpos, dform, dpos, direction, distance)
    yield u'1,3,4,dir,dist:{0},{1},{2},{3},{4}'.format(hform, dform, dpos, direction, distance)
    yield u'1,2,3,dir,dist:{0},{1},{2},{3},{4}'.format(hform, hpos, dform, direction, distance)
    yield u'1,2,4,dir,dist:{0},{1},{2},{3},{4}'.format(hform, hpos, dpos, direction, distance)
    yield u'2,5,4,dir,dist:{0},{1},{2},{3},{4}'.format(hpos, bpos, dpos, direction, distance)
    yield u'2,5,3,dir,dist:{0},{1},{2},{3},{4}'.format(hpos, bpos, dform, direction, distance)
    yield u'1,5,4,dir,dist:{0},{1},{2},{3},{4}'.format(hform, bpos, dpos, direction, distance)
    yield u'1,5,3,dir,dist:{0},{1},{2},{3},{4}'.format(hform, bpos, dform, direction, distance)

    yield u'6,2,7,4,dir,dist:{0},{1},{2},{3},{4},{5}'.format(hlemma, hpos, dlemma, dpos, direction, distance)
    yield u'2,7,4,dir,dist:{0},{1},{2},{3},{4}'.format(hpos, dlemma, dpos, direction, distance)
    yield u'6,7,4,dir,dist:{0},{1},{2},{3},{4}'.format(hlemma, dlemma, dpos, direction, distance)
    yield u'6,2,7,dir,dist:{0},{1},{2},{3},{4}'.format(hlemma, hpos, dlemma, direction, distance)
    yield u'6,2,4,dir,dist:{0},{1},{2},{3},{4}'.format(hlemma, hpos, dpos, direction, distance)
    yield u'2,5,7,dir,dist:{0},{1},{2},{3},{4}'.format(hpos, bpos, dlemma, direction, distance)
    yield u'6,5,4,dir,dist:{0},{1},{2},{3},{4}'.format(hlemma, bpos, dpos, direction, distance)
    yield u'6,5,7,dir,dist:{0},{1},{2},{3},{4}'.format(hlemma, bpos, dlemma, direction, distance)


def give_distance(id1, id2, direction):

    if direction == "right":
        d = id1 - id2
    else:
        d = id2 - id1

    if d < 1:
        print "Error in distance computing, distance is too low."
        distance = "__ERROR__"
    elif d == 1:
        distance = "1"
    elif d == 2:
        distance = "2"
    elif d == 3:
        distance = "3"
    elif d == 4:
        distance = "4"
    elif d == 5:
        distance = "5"
    elif 5 < d <= 10:
        distance = "6-10"
    elif 10 < d <= 20:
        distance = "11-20"
    else:
        distance = ">20"
    
    return distance


def give_direction(id1, id2):
    if id2 < id1:
        direction = "right"
    else:
        direction = "left"

    return direction


def fm(infile):

    # takes a file in conll06 format, returns a feature map
    feat_map = {}  # featmap as dictionary {feature:index}
    index = 0  # index in featmap

    for sentence in sentences(codecs.open(infile, encoding='utf-8')):
        for token1 in sentence:
            direction = "left"
            distance = give_distance(0, token1.id, direction)
            # add root features
            for feature in give_features("__ROOT__", "__ROOT__", "__ROOT__", token1.form, token1.lemma, token1.pos,
                                         token1.rel, direction, distance):
                if feature not in feat_map:
                    feat_map[feature] = index
                    index += 1

            # add other features
            for token2 in (token2 for token2 in sentence if token2.id != token1.id):

                # direction
                direction = give_direction(token1.id, token2.id)

                # distance
                distance = give_distance(token1.id, token2.id, direction)

                for feature in give_features(token1.form, token1.lemma, token1.pos, token2.form, token2.lemma,
                                             token2.pos, token2.rel, direction, distance):
                    if feature not in feat_map:
                        feat_map[feature] = index
                        index += 1

    return feat_map
