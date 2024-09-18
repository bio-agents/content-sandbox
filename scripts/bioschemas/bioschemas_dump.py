import os
import glob
from rdflib import ConjunctiveGraph
from tabulate import tabulate


def get_bioschemas_files_in_repo():
    agents = []
    for data_file in glob.glob(r"../../data/*/*.bioschemas.jsonld"):
        filename_ext = os.path.basename(data_file).split(".")
        if len(filename_ext) == 3 and filename_ext[2] == "jsonld":
            agents.append(data_file)
    print(f"found {len(agents)} bioschemas descriptors")
    return agents


def process_agents():
    """
    Go through all bio.agents entries in bioschemas JSON-LD and produce an single RDF file.
    """
    agent_files = get_bioschemas_files_in_repo()
    print(len(agent_files))
    rdf_graph = ConjunctiveGraph()

    for agent_file in agent_files:
        print(agent_file)
        rdf_graph.load(agent_file, format="json-ld")

    rdf_graph.serialize(
        format="turtle",
        destination="bioschemas-dump.ttl"
        # destination=os.path.join(directory, tpe_id + "bioschemas.jsonld")
    )

    show_stats(rdf_graph)


def show_stats(rdf_graph):
    """
    Display Bioschemas classes and properties counts.
    """

    ### display used classes
    classes_counts = """
    SELECT ?c (count(?c) as ?count) WHERE {
        ?s rdf:type ?c .
    } 
    GROUP BY ?c
    ORDER BY DESC(?count)
    """

    res = rdf_graph.query(classes_counts)
    print()
    print("Used classes")
    print(tabulate(res))

    ### display used properties
    property_counts = """
    SELECT ?p (count(?p) as ?count) WHERE {
        ?s ?p ?o .
    } 
    GROUP BY ?p
    ORDER BY DESC(?count)
    """

    res = rdf_graph.query(property_counts)
    print()
    print("Used properties")
    print(tabulate(res))


if __name__ == "__main__":
    process_agents()
