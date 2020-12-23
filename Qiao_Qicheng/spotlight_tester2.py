from SPARQLWrapper import SPARQLWrapper

queryString = "SELECT * WHERE { ?s ?p ?o. }"
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

sparql.setQuery(queryString)

try :
   ret = sparql.query()
   # ret is a stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
except :
   print("error")