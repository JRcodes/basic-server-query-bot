import os, sys, json
from server_query import ServerQuery


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
file_name = sys.argv[1]
file_path = f"{ROOT_DIR}/{file_name}"


def json_dumper(dict_object):
    output_file_path = f"{ROOT_DIR}/output.json"
    with open(output_file_path, "w") as output_file:
        json.dump(dict_object, output_file)
    pass


def main():
    querybot = ServerQuery()
    output = querybot.main(file_path)
    json_dumper(dict_object=output)


if __name__ == "__main__":
    main()
