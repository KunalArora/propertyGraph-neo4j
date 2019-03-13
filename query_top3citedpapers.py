from py2neo import Graph, Database

db = Database()
graph = Graph(user="neo4j")


def top3CitedPapersOfConf():
    query = """
    MATCH (c:conference)--(p:paper)<--(p2:paper)
    WITH c.name as confName, p.title as paperName, count(p2.title ) as nCitation
    ORDER BY confName, nCitation desc
    WITH confName, collect(paperName) as citation
    return confName, citation[..3] as Top3CitedPapers
    """
    return graph.run(query).data()


if __name__ == '__main__':
    list_citedPapers = top3CitedPapersOfConf()
    print("List of conference name and their top 3 cited papers")
    for val in list_citedPapers:
        print(val)

