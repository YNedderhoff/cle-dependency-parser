from token import sentences
import codecs

def fm (infile):
    # takes a file in conll09 format, returns a feature map
    feat_map = {}  # featmap as dictionary {feature:index}
    index = 0  # index in featmap
    for sentence in sentences(codecs.open(infile,encoding='utf-8')):
        local_features=[]
        for token1 in sentence:
            if token1.head == 0:
                # at this point ROOT is the head and token1 is the dependent
                
                # unigram features
                local_features.append("hform:__ROOT__")
                local_features.append("dform:"+token1.form)
                local_features.append("dpos:"+token1.pos)
                local_features.append("hform,dpos:"+"__ROOT__"+","+token1.pos)
                local_features.append("dform,dpos:"+token1.form+","+token1.pos)
                local_features.append("bpos:"+token1.rel)

                # bigram features
                local_features.append("hform,dform,dpos:"+"__ROOT__"+","+token1.form+","+token1.pos)
                local_features.append("hform,dform:"+"__ROOT__"+","+token1.form)

                # other
                local_features.append("hform,bpos,dpos:"+"__ROOT__"+","+token1.rel+","+token1.pos)
                local_features.append("hform,bpos,dform:"+"__ROOT__"+","+token1.rel+","+token1.form)
        for token1 in sentence:
            for token2 in sentence:
                if token2.head == token1.id:
                    # at this point, token1 is the head, and token2 the dependent

                    # unigram features
                    local_features.append("hform:"+token1.form)
                    local_features.append("hpos:"+token1.pos)
                    local_features.append("dform:"+token2.form)
                    local_features.append("dpos:"+token2.pos)
                    local_features.append("hform,dpos:"+token1.form+","+token2.pos)
                    local_features.append("hpos,dform:"+token1.pos+","+token2.form)
                    local_features.append("hform,hpos:"+token1.form+","+token1.pos)
                    local_features.append("dform,dpos:"+token2.form+","+token2.pos)
                    local_features.append("bpos:"+token2.rel)

                    # bigram features
                    local_features.append("hform,hpos,dform,dpos:"+token1.form+","+token1.pos+","+token2.form+","+token2.pos)
                    local_features.append("hpos,dform,dpos:"+token1.pos+","+token2.form+","+token2.pos)
                    local_features.append("hform,dform,dpos:"+token1.form+","+token2.form+","+token2.pos)
                    local_features.append("hform,hpos,dform:"+token1.form+","+token1.pos+","+token2.form)
                    local_features.append("hform,hpos,dpos:"+token1.form+","+token1.pos+","+token2.pos)
                    local_features.append("hform,dform:"+token1.form+","+token2.form)
                    local_features.append("hpos,dpos:"+token1.pos+","+token2.pos)

                    # other
                    local_features.append("hpos,bpos,dpos:"+token1.pos+","+token2.rel+","+token2.pos)
                    local_features.append("hpos,bpos,dform:"+token1.pos+","+token2.rel+","+token2.form)
                    local_features.append("hform,bpos,dpos:"+token1.form+","+token2.rel+","+token2.pos)
                    local_features.append("hform,bpos,dform:"+token1.form+","+token2.rel+","+token2.form)
        for feature in local_features:
            if not feature in feat_map:
                feat_map[feature]=index
                index += 1
    return feat_map

def add_feat_vec_to_sparse_graph(full_graph, sparse_graph, feat_map):

    for head in full_graph:
        for full_arc in full_graph[head]:

            feat_v = fill_feat_vec(full_arc, feat_map)

            for sparse_arc in sparse_graph[head]:
                if sparse_arc.dependent == full_arc.dependent:
                    sparse_arc.feat_vec = feat_v

    return sparse_graph

def add_feat_vec_to_full_graph(full_graph, feat_map):
    for head in full_graph:
        for full_arc in full_graph[head]:

            full_arc.feat_vec = fill_feat_vec(full_arc, feat_map)

    return full_graph

def reverse_feat_map(feat_map):
    rev_feat_map = {}
    for feature in feat_map:
        rev_feat_map[feat_map[feature]] = feature
    return rev_feat_map


def fill_feat_vec(arc, feat_map):

    # checks for the arc if the features are in the feature representation and returns it's feature vector

    feat_v = []

    # unigram features

    if "hform:"+arc.head_form in feat_map:
        feat_v.append(feat_map["hform:"+arc.head_form])
    if "hpos:"+arc.head_pos in feat_map:
        feat_v.append(feat_map["hpos:"+arc.head_pos])
    if "dform:"+arc.dependent_form in feat_map:
        feat_v.append(feat_map["dform:"+arc.dependent_form])
    if "dpos:"+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["dpos:"+arc.dependent_pos])
    if "hform,dpos:"+arc.head_form+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["hform,dpos:"+arc.head_form+","+arc.dependent_pos])
    if "hpos,dform:"+arc.head_pos+","+arc.dependent_form in feat_map:
        feat_v.append(feat_map["hpos,dform:"+arc.head_pos+","+arc.dependent_form])
    if "hform,hpos:"+arc.head_form+","+arc.head_pos in feat_map:
        feat_v.append(feat_map["hform,hpos:"+arc.head_form+","+arc.head_pos])
    if "dform,dpos:"+arc.dependent_form+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["dform,dpos:"+arc.dependent_form+","+arc.dependent_pos])
    if "bpos:"+arc.rel in feat_map:
        feat_v.append(feat_map["bpos:"+arc.rel])

    # bigram features

    if "hform,hpos,dform,dpos:"+arc.head_form+","+arc.head_pos+","+arc.dependent_form+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["hform,hpos,dform,dpos:"+arc.head_form+","+arc.head_pos+","+arc.dependent_form+","+arc.dependent_pos])
    if "hpos,dform,dpos:"+arc.head_pos+","+arc.dependent_form+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["hpos,dform,dpos:"+arc.head_pos+","+arc.dependent_form+","+arc.dependent_pos])
    if "hform,dform,dpos:"+arc.head_form+","+arc.dependent_form+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["hform,dform,dpos:"+arc.head_form+","+arc.dependent_form+","+arc.dependent_pos])
    if "hform,hpos,dform:"+arc.head_form+","+arc.head_pos+","+arc.dependent_form in feat_map:
        feat_v.append(feat_map["hform,hpos,dform:"+arc.head_form+","+arc.head_pos+","+arc.dependent_form])
    if "hform,hpos,dpos:"+arc.head_form+","+arc.head_pos+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["hform,hpos,dpos:"+arc.head_form+","+arc.head_pos+","+arc.dependent_pos])
    if "hform,dform:"+arc.head_form+","+arc.dependent_form in feat_map:
        feat_v.append(feat_map["hform,dform:"+arc.head_form+","+arc.dependent_form])
    if "hpos,dpos:"+arc.head_pos+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["hpos,dpos:"+arc.head_pos+","+arc.dependent_pos])

    # other
    
    if "hpos,bpos,dpos:"+arc.head_pos+","+arc.rel+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["hpos,bpos,dpos:"+arc.head_pos+","+arc.rel+","+arc.dependent_pos])
    if "hpos,bpos,dform:"+arc.head_pos+","+arc.rel+","+arc.dependent_form in feat_map:
        feat_v.append(feat_map["hpos,bpos,dform:"+arc.head_pos+","+arc.rel+","+arc.dependent_form])
    if "hform,bpos,dpos:"+arc.head_form+","+arc.rel+","+arc.dependent_pos in feat_map:
        feat_v.append(feat_map["hform,bpos,dpos:"+arc.head_form+","+arc.rel+","+arc.dependent_pos])
    if "hform,bpos,dform:"+arc.head_form+","+arc.rel+","+arc.dependent_form in feat_map:
        feat_v.append(feat_map["hform,bpos,dform:"+arc.head_form+","+arc.rel+","+arc.dependent_form])

    return feat_v