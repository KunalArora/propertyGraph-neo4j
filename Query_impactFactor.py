from py2neo import Graph, Database

db = Database()
graph = Graph(user="neo4j")


def journal_impactFactor():
    query = """
    MATCH (j:journal)-[r:volume]-()--(a:author)--(p:paper)<-[:has_citation]-(p2:paper)
    WITH j.name as journalName, a.authorName as authorName, r.year as jYear, count(p2.title) as citation
    WHERE jYear in [(date().year-1), (date().year-2)]
    RETURN journalName,  sum(citation)/count(authorName)  as ImpactFactor
    ORDER BY ImpactFactor DESC
    """
    return graph.run(query).data()


if __name__ == '__main__':
    list_impactFactor = journal_impactFactor()
    print("List of journal name and their Impact Factor")
    for val in list_impactFactor:
        print(val)

