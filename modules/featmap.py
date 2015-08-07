from token import sentences
import codecs


def give_features(hform, hlemma, hpos, dform, dlemma, dpos, hrform, hrpos, hlform, hlpos, drform, drpos, dlform, dlpos,
                  direction, distance):
    # generator that yields features based on the following information:

    # 1 = hform = form of the head
    # 2 = hpos = pos of the head
    # 3 = dform = form of the dependent
    # 4 = dpos = pos of the dependent
    # 5 = hlemma = lemma of the head
    # 6 = dlemma = lemma of the dependent

    # 7 = hrform = form of the right neighbour of the head
    # 8 = hrpos = pos of the right neighbour of the head
    # 9 = hlform = form of the left neighbour of the head
    # 10 = hlpos = pos of the left neighbour of the head
    # 11 = drform = form of the right neighbour of the dependent
    # 12 = drpos = pos of the right neighbour of the dependent
    # 13 = dlform = form of the left neighbour of the dependent
    # 14 = dlpos = pos of the left neighbour of the dependent

    # 15 = direction = is the head right or left of the dependent in the sentence
    # 16 = distance = the distance between head and dependent

    yield u'1,15,16:{0},{1},{2}'.format(hform, direction, distance)
    yield u'2,15,16:{0},{1},{2}'.format(hpos, direction, distance)
    yield u'3,15,16:{0},{1},{2}'.format(dform, direction, distance)
    yield u'4,15,16:{0},{1},{2}'.format(dpos, direction, distance)
    yield u'5,15,16:{0},{1},{2}'.format(hlemma, direction, distance)
    yield u'6,15,16:{0},{1},{2}'.format(dlemma, direction, distance)

    yield u'1,4,15,16:{0},{1},{2},{3}'.format(hform, dpos, direction, distance)
    yield u'2,3,15,16:{0},{1},{2},{3}'.format(hpos, dform, direction, distance)
    yield u'1,2,15,16:{0},{1},{2},{3}'.format(hform, hpos, direction, distance)
    yield u'3,4,15,16:{0},{1},{2},{3}'.format(dform, dpos, direction, distance)
    yield u'1,3,15,16:{0},{1},{2},{3}'.format(hform, dform, direction, distance)
    yield u'2,4,15,16:{0},{1},{2},{3}'.format(hpos, dpos, direction, distance)
    yield u'5,4,15,16:{0},{1},{2},{3}'.format(hlemma, dpos, direction, distance)
    yield u'2,6,15,16:{0},{1},{2},{3}'.format(hpos, dlemma, direction, distance)
    yield u'5,2,15,16:{0},{1},{2},{3}'.format(hlemma, hpos, direction, distance)
    yield u'6,4,15,16:{0},{1},{2},{3}'.format(dlemma, dpos, direction, distance)
    yield u'5,6,15,16:{0},{1},{2},{3}'.format(hlemma, dlemma, direction, distance)

    yield u'1,2,3,4,15,16:{0},{1},{2},{3},{4},{5}'.format(hform, hpos, dform, dpos, direction, distance)
    yield u'2,3,4,15,16:{0},{1},{2},{3},{4}'.format(hpos, dform, dpos, direction, distance)
    yield u'1,3,4,15,16:{0},{1},{2},{3},{4}'.format(hform, dform, dpos, direction, distance)
    yield u'1,2,3,15,16:{0},{1},{2},{3},{4}'.format(hform, hpos, dform, direction, distance)
    yield u'1,2,4,15,16:{0},{1},{2},{3},{4}'.format(hform, hpos, dpos, direction, distance)

    yield u'5,2,6,4,15,16:{0},{1},{2},{3},{4},{5}'.format(hlemma, hpos, dlemma, dpos, direction, distance)
    yield u'2,6,4,15,16:{0},{1},{2},{3},{4}'.format(hpos, dlemma, dpos, direction, distance)
    yield u'5,6,4,15,16:{0},{1},{2},{3},{4}'.format(hlemma, dlemma, dpos, direction, distance)
    yield u'5,2,6,15,16:{0},{1},{2},{3},{4}'.format(hlemma, hpos, dlemma, direction, distance)
    yield u'5,2,4,15,16:{0},{1},{2},{3},{4}'.format(hlemma, hpos, dpos, direction, distance)

    if hrform != "__NULL__":
        yield u'7,15,16:{0},{1},{2}'.format(hrform, direction, distance)
        yield u'1,7,15,16:{0},{1},{2},{3}'.format(hform, hrform, direction, distance)
    if hrpos != "__NULL__":
        yield u'8,15,16:{0},{1},{2}'.format(hrpos, direction, distance)
        yield u'2,8,15,16:{0},{1},{2},{3}'.format(hpos, hrpos, direction, distance)
    if hlform != "__NULL__":
        yield u'9,15,16:{0},{1},{2}'.format(hlform, direction, distance)
        yield u'9,1,15,16:{0},{1},{2},{3}'.format(hlform, hform, direction, distance)
    if hlpos != "__NULL__":
        yield u'10,15,16:{0},{1},{2}'.format(hlpos, direction, distance)
        yield u'10,2,15,16:{0},{1},{2},{3}'.format(hlpos, hpos, direction, distance)
    if drform != "__NULL__":
        yield u'11,15,16:{0},{1},{2}'.format(drform, direction, distance)
        yield u'3,11,15,16:{0},{1},{2},{3}'.format(dform, drform, direction, distance)
    if drpos != "__NULL__":
        yield u'12,15,16:{0},{1},{2}'.format(drpos, direction, distance)
        yield u'4,12,15,16:{0},{1},{2},{3}'.format(dpos, drpos, direction, distance)
    if dlform != "__NULL__":
        yield u'13,15,16:{0},{1},{2}'.format(dlform, direction, distance)
        yield u'13,3,15,16:{0},{1},{2},{3}'.format(dlform, dform, direction, distance)
    if dlpos != "__NULL__":
        yield u'14,15,16:{0},{1},{2}'.format(dlpos, direction, distance)
        yield u'14,4,15,16:{0},{1},{2},{3}'.format(dlpos, dpos, direction, distance)
    if hlform != "__NULL__" and hrform != "__NULL":
        yield u'9,1,7,15,16:{0},{1},{2},{3},{4}'.format(hlform, hform, hrform, direction, distance)
    if hlpos != "__NULL__" and hrpos != "__NULL":
        yield u'10,2,8,15,16:{0},{1},{2},{3},{4}'.format(hlpos, hpos, hrpos, direction, distance)
    if dlform != "__NULL__" and drform != "__NULL":
        yield u'13,3,11,15,16:{0},{1},{2},{3},{4}'.format(dlform, dform, drform, direction, distance)
    if dlpos != "__NULL__" and drpos != "__NULL__":
        yield u'14,4,12,15,16:{0},{1},{2},{3},{4}'.format(dlpos, dpos, drpos, direction, distance)


def give_distance(id1, id2, direction):

    # returns the distance of head and dependent in the sentence as bucketed feature

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

    # returns the direction of the head (left or right from the dependent)

    if id2 < id1:
        direction = "right"
    else:
        direction = "left"

    return direction


def give_surrounding_information(sentence, id1, id2):

    # returns form and pos of the left and right neighbours of head and dependent

    hrform = "__NULL__"
    hrpos = "__NULL__"
    hlform = "__NULL__"
    hlpos = "__NULL__"

    drform = "__NULL__"
    drpos = "__NULL__"
    dlform = "__NULL__"
    dlpos = "__NULL__"

    if id1 not in [0, 1, len(sentence)]:
        hrform = sentence[id1].form
        hrpos = sentence[id1].pos
        hlform = sentence[id1 - 2].form
        hlpos = sentence[id1 - 2].pos
    elif id1 == 0:
        hrform = sentence[id1].form
        hrpos = sentence[id1].pos
    elif id1 == 1:
        hrform = sentence[id1].form
        hrpos = sentence[id1].pos
    elif id1 == len(sentence):
        hlform = sentence[id1 - 2].form
        hlpos = sentence[id1 - 2].pos

    if id2 not in [0, 1, len(sentence)]:
        drform = sentence[id2].form
        drpos = sentence[id2].pos
        dlform = sentence[id2 - 2].form
        dlpos = sentence[id2 - 2].pos
    elif id2 == 0:
        drform = sentence[id2].form
        drpos = sentence[id2].pos
    elif id2 == 1:
        drform = sentence[id2].form
        drpos = sentence[id2].pos
    elif id2 == len(sentence):
        dlform = sentence[id2 - 2].form
        dlpos = sentence[id2 - 2].pos

    return hrform, hrpos, hlform, hlpos, drform, drpos, dlform, dlpos


def fm(infile):
    # takes a file in conll06 format, returns a feature map
    feat_map = {}  # featmap as dictionary {feature:index}
    index = 0  # index in featmap

    for sentence in sentences(codecs.open(infile, encoding='utf-8')):
        for token1 in sentence:

            direction = "left"
            distance = give_distance(0, token1.id, direction)
            hrform = hrpos = hlform = hlpos = drform = drpos = dlform = dlpos = "__NULL__"

            # add root features
            for feature in give_features("__ROOT__", "__ROOT__", "__ROOT__", token1.form, token1.lemma, token1.pos,
                                         hrform, hrpos, hlform, hlpos, drform, drpos, dlform, dlpos, direction,
                                         distance):

                if feature not in feat_map:
                    feat_map[feature] = index
                    index += 1

            # add other features
            for token2 in (token2 for token2 in sentence if token2.id != token1.id):

                direction = give_direction(token1.id, token2.id)
                distance = give_distance(token1.id, token2.id, direction)
                hrform, hrpos, hlform, hlpos, drform, drpos, dlform, dlpos = give_surrounding_information(sentence,
                                                                                                          token1.id,
                                                                                                          token2.id)

                for feature in give_features(token1.form, token1.lemma, token1.pos, token2.form, token2.lemma,
                                             token2.pos, hrform, hrpos, hlform, hlpos, drform, drpos, dlform, dlpos,
                                             direction, distance):

                    if feature not in feat_map:
                        feat_map[feature] = index
                        index += 1

    return feat_map
