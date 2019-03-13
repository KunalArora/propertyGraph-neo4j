from py2neo import Graph, Database

db = Database()
graph = Graph(user="neo4j")


def confCommuntity():
    query = """
    MATCH (c:conference)-[r:edition]->(p:paper)<--(a:author)
    WITH c.name as confName, a.authorName as authorName, count(distinct r.year) as nYear
    WHERE nYear>=4
    RETURN confName, collect(authorName) as authorNames
    """
    return graph.run(query).data()


if __name__ == '__main__':
    list_confComm= confCommuntity()
    print("List of conference name and their community authors with papers in 4 different editions.")
    for val in list_confComm:
        print(val)

