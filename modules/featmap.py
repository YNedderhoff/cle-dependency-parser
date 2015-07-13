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
                local_features.append("hform:Root")
                local_features.append("hpos:__NULL__")
                local_features.append("dform:"+token1.form)
                local_features.append("dpos:"+token1.pos)
                local_features.append("hform,dpos:"+"Root"+","+token1.pos)
                local_features.append("hpos,dform:"+"__NULL__"+","+token1.form)
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
