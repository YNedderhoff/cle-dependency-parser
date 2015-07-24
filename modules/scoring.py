def score(graph, weight_vector):
    for head in graph:
        for arc in graph[head]:
            s = 0.0
            for feature in arc.feat_vec:
                s += weight_vector[feature]
            arc.score = s
    return graph
