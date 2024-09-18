import json
import os
import sys
import glob
import argparse

import requests
from boltons.iterutils import remap

def clean():
    for data_file in glob.glob(r"../../data/*/*.json"):
        filename_ext = os.path.basename(data_file).split(".")
        if len(filename_ext) == 2 and filename_ext[1] == "json":
            os.remove(data_file)


def retrieve(filters=None):
    """
    Go through bio.agents entries using its API and save the JSON files
    in the right folders
    """

    i = 1
    nb_agents = 1
    has_next_page = True
    filters = filters or {}
    while has_next_page:
        parameters = {**filters, **{"page": i}}
        response = requests.get(
            "https://ecosystem.bio.agents/api/agent/",
            params=parameters,
            headers={"Accept": "application/json"},
        )
        try:
            entry = response.json()
        except JSONDecodeError as e:
            print("Json decode error for " + str(req.data.decode("utf-8")))
            break
        has_next_page = entry["next"] != None

        for agent in entry["list"]:
            agent_id = agent["bioagentsID"]
            tpe_id = agent_id.lower()
            directory = os.path.join("..", "..", "data", tpe_id)
            if not os.path.isdir(directory):
                os.mkdir(directory)
            with open(os.path.join(directory, tpe_id + ".bioagents.json"), "w") as write_file:
                drop_false = lambda path, key, value: bool(value)
                agent_cleaned = remap(agent, visit=drop_false)
                json.dump(
                    agent_cleaned, write_file, sort_keys=True, indent=4, separators=(",", ": ")
                )
            nb_agents += 1
            print(f"import agent #{nb_agents}: {agent_id} in folder {directory}")
        i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="bioagents import")
    parser.add_argument(
        "collection", type=str, default="*", nargs="?", help="collection name filter"
    )
    args = parser.parse_args()
    clean()
    if args.collection == "*":
        retrieve()
    else:
        retrieve(filters={"collection": args.collection})
