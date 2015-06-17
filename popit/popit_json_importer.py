__author__ = 'sweemeng'
import json
import requests
import argparse
import logging
import re

def main():
    parser = argparse.ArgumentParser("PopIt Importer")
    parser.add_argument("--source", dest="source", help="PopIt instance to import from")
    parser.add_argument("--destination", dest="destination", help="Destination to export to")
    parser.add_argument("--apikey", dest="apikey", help="API Key to destination")

    args = parser.parse_args()
    entities = ["organizations", "persons", "posts", "memberships"]
    logging.info(args.source)
    data = json.load(open(args.source))
    destination = args.destination
    apikey = args.apikey
    for entity in entities:
        create_entity(data, destination, entity, apikey)

def create_entity(data, destination, entity, api_key):
    destination_endpoint = "%s/%s" % (destination, entity)

    headers = { "Apikey": api_key, "Content-Type":"application/json"}
    for entry in data[entity]:
        temp = data_messager(entry, entry)
        # Because membership is it's own entity
        logging.warning("Endpoint: %s" % destination_endpoint)
        logging.warning("Entity: %s" % entity, )
        logging.warning("Data: %s" % json.dumps(temp))
        destination_query = requests.post(destination_endpoint, data=json.dumps(temp), headers=headers)

        if destination_query.status_code != 200:
            raise Exception(destination_query.content)

def data_messager(data, parent):
    for key in data:
        logging.warning("%s:%s" % (key,data[key]))
        if type(data[key]) is list:
            for item in data[key]:
                if item:
                    item = data_messager(item, key)
        if key in ("birth_date", "death_date", "start_date", "end_date", "founding_date", "dissolution_date"):
            if not data[key]:
                data[key] = "0000-00-00"
            if not re.match("^[0-9]{4}(-[0-9]{2}){0,2}$", data[key]):
                data[key] = "0000-00-00"
            else:
                splitted =  data[key].split("-")
                new_split = []
                for s in splitted:
                    if len(s) == 1:
                        new_split.append("0"+s)
                    else:
                        new_split.append(s)

                data[key] = "-".join(new_split)
                logging.warning("new value %s" % data[key])

    if parent != "links" and "url" in data:
        del data["url"]
    if parent != "links" and "html_url" in data:
        del data["html_url"]

    if data.get("area") and not data.get("area").get("id"):
        del data["area"]


    return data

if __name__ == "__main__":
    main()
