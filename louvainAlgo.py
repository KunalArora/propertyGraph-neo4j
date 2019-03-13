from py2neo import Graph, Database

db = Database()
graph = Graph(user="neo4j")


def louvainAlgo():
    query = """
    CALL algo.louvain.stream('paper', 'has_citation', {})
    YIELD nodeId, community
    RETURN algo.getNodeById(nodeId).title AS user, community
    ORDER BY community;
    """
    return graph.run(query).data()


if __name__ == '__main__':
    list_community = louvainAlgo()
    print("List of papers and their page rank score ")
    for val in list_community:
        print(val)

