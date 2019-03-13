from py2neo import Graph, Database

db = Database()
graph = Graph(user="neo4j")


def pageRankAlgo():
    query = """
    CALL algo.pageRank.stream('paper', 'has_citation', {iterations:20, dampingFactor:0.85})
    YIELD nodeId, score
    RETURN algo.getNodeById(node.Id).title AS page, score
    ORDER BY score DESC
    """
    return graph.run(query).data()


if __name__ == '__main__':
    list_score = pageRankAlgo()
    print("List of papers and their page rank score ")
    for val in list_score:
        print(val)

