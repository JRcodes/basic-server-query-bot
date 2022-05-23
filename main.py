import os, sys, json, logging
from server_query import ServerQuery

logging.basicConfig(
    level=logging.INFO,
    filemode="w",
    format="%(levelname)s %(message)s",
)

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
file_name = sys.argv[1]
file_path = f"{ROOT_DIR}/{file_name}"


def json_dumper(dict_object):
    """
    This function receives a dictionary object and dumps it into a json file at
    the project root
    Parameters:
    -----------
    dict_object: dict
        a python dictionary

    Returns:
    --------
    None
    """
    output_file_path = f"{ROOT_DIR}/output.json"
    with open(output_file_path, "w") as output_file:
        json.dump(dict_object, output_file)


def main():
    """
    This is the entry point of the application. It calls the ServerQuery class
    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """
    querybot = ServerQuery()
    output = querybot.main(file_path)
    json_dumper(dict_object=output)


if __name__ == "__main__":
    logging.info("STARTING QUERY JOB ... \n")
    main()
    logging.info("QUERY JOB COMPLETE")
