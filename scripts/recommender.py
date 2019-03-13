from py2neo import Graph, Database

db = Database()
graph = Graph(user="neo4j")

database_keywords = [
    "Data Management",
    "Semantic Data",
    "Data Modeling",
    "Big Data",
    "Data Processing",
    "Data Storage",
    "Data Querying"
]

# Finding the papers of a certain community
def get_community():
    query = """
    Match(p:paper)-->(k:keyword)
    Where k.keywordName IN """ + str(database_keywords) + """
    return collect(distinct p.title) as ListOfPapersInCommunity
    """
    return graph.run(query).data()


# Part B Finding research communities for community with given keywords We pipeline the results of the first and
# second query. This function will return all those conferences that have papers belonging to the research community
# as specified by community threshold
def get_research_community_conferences(keywords):
    query = """
                MATCH (c1:conference)-->(p2:paper) with c1.name as confName, count(distinct p2.title) as TotalCountOfPapersInConf
                MATCH (c:conference)-->(p:paper)-->(k:keyword)
                WHERE k.keywordName IN """ + str(database_keywords) + """ and confName = c.name with c, TotalCountOfPapersInConf,
                collect(distinct p.title) as ListOfConfPapersInComm, count(distinct p.title) As TotalConfPaperInCommunity 
                WHERE (toFloat(TotalConfPaperInCommunity)/toFloat(TotalCountOfPapersInConf)>=0.9) 
                RETURN c.name as confName, TotalConfPaperInCommunity, TotalCountOfPapersInConf, ListOfConfPapersInComm
            """
    return graph.run(query).data()


# Page rank algorithm returning the Top 100 papers of all the conferences which has more than 90% of their papers
# in the community and also, most of the citations of their paper is from that community
def run_page_rank(all_papers):
    query = """
            CALL algo.pageRank.stream('article', 'has_citation', {iterations:1, dampingFactor:0.85})
            YIELD nodeId, score
            WITH algo.getNodeById(nodeId).title AS page,score
            WHERE page IN """ + str(all_papers) + """
            RETURN page, score
            ORDER BY score DESC LIMIT 50
            """
    return graph.run(query).data()


# Final step to get gurus which is the authors having atleast 2 papers in the top 100 papers
def get_gurus(listOfTop100Papers):
    query = """
    Match(a:author)-[w:wrote]->(p:paper) 
    WHERE p.title IN """ + str(listOfTop100Papers) + """ 
    WITH a.authorName as authorNames, count(w)>=2 as NoOfArticlesWrote LIMIT 10
    RETURN collect(authorNames) as Gurus 
    """
    return graph.run(query).data()


if __name__ == '__main__':
    all_community_papers = get_community()
    list_all_community_papers=[]
    for paper in all_community_papers:
        for value in paper["ListOfPapersInCommunity"]:
            list_all_community_papers.append(value)

    community_conferences = get_research_community_conferences(database_keywords)
    conferences_papers = {}
    for conf in community_conferences:
        conferences_papers[conf["confName"]] = conf["ListOfConfPapersInComm"]

    result = run_page_rank(list_all_community_papers)
    listOfTop100Papers = []
    for val in result:
        listOfTop100Papers.append(val['page'])
    print("-----------List of Top 100 papers:--------------")
    print(listOfTop100Papers)

    print("-----------Gurus-----------------")
    gurus = get_gurus(listOfTop100Papers)
    print(gurus)








