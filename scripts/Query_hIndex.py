from py2neo import Graph, Database

db = Database()
graph = Graph(user="neo4j")


def authors_h_index():
    query = """
    MATCH (a:author)-[rw:wrote]->(p:paper)<-[rc:has_citation]-(c:paper)
    WITH a.authorName as authorName, p.title as paperName,
        count(c.title) as nCitation
    ORDER BY authorName, nCitation DESC
    WITH authorName, collect(nCitation) as citation
    UNWIND range(0, size(citation)-1) as position WITH authorName,
    CASE WHEN citation[position] <= (position+1)
        THEN citation[position]
        ELSE (position+1)
    END as index
    RETURN authorName, max(index) as hIndex
    """
    return graph.run(query).data()


if __name__ == '__main__':
    list_h_index = authors_h_index()
    print("List of author name and their H-index")
    for val in list_h_index:
        print(val)

