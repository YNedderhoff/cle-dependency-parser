from token import sentences
import codecs

def fm (infile):
    # takes a file in conll09 format, returns a feature map
    feat_map = {}  # featmap as dictionary {feature:index}
    index = 0  # index in featmap
    for sentence in sentences(codecs.open(infile,encoding='utf-8')):
        local_features=[]
        for token1 in sentence:
            if int(token1.head) == 0:
                # at this point ROOT is the head and token1 is the dependent
                local_features.append("hform:__ROOT__")
                local_features.append("dform:"+token1.form)
                local_features.append("dpos:"+token1.pos)
                local_features.append("hform,dpos:"+"__ROOT__"+","+token1.pos)
        for token1 in sentence:
            for token2 in sentence:
                if token2.head == token1.id:
                    # at this point, token1 is the head, and token2 the dependent
                    local_features.append("hform:"+token1.form)
                    local_features.append("hpos:"+token1.pos)
                    local_features.append("dform:"+token2.form)
                    local_features.append("dpos:"+token2.pos)
                    local_features.append("hform,dpos:"+token1.form+","+token2.pos)
                    local_features.append("hpos,dform:"+token1.pos+","+token2.form)
        for feature in local_features:
            if not feature in feat_map:
                feat_map[feature]=index
                index += 1
    return feat_map

def add_feat_vec(full_graph, sparse_graph, feat_map):
    for head in full_graph:
        for full_arc in full_graph[head]:
            feat_v = []
            if "hform:"+full_arc.head_form in feat_map:
                feat_v.append(feat_map["hform:"+full_arc.head_form])
            if "hpos:"+full_arc.head_pos in feat_map:
                feat_v.append(feat_map["hpos:"+full_arc.head_pos])
            if "dform:"+full_arc.dependent_form in feat_map:
                feat_v.append(feat_map["dform:"+full_arc.dependent_form])
            if "dpos:"+full_arc.dependent_pos in feat_map:
                feat_v.append(feat_map["dpos:"+full_arc.dependent_pos])
            if "hform,dpos:"+full_arc.head_form+","+full_arc.dependent_pos in feat_map:
                feat_v.append(feat_map["hform,dpos:"+full_arc.head_form+","+full_arc.dependent_pos])
            if "hpos,dform:"+full_arc.head_pos+","+full_arc.dependent_form in feat_map:
                feat_v.append(feat_map["hpos,dform:"+full_arc.head_pos+","+full_arc.dependent_form])

            for sparse_arc in sparse_graph[head]:
                if sparse_arc.dependent == full_arc.dependent:
                    sparse_arc.feat_vec = feat_v

    return sparse_graph

def reverse_feat_map(feat_map):
    rev_feat_map = {}
    for feature in feat_map:
        rev_feat_map[feat_map[feature]] = feature
    return rev_feat_map
