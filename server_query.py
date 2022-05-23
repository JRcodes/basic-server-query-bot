import logging, requests, os, json

logging.basicConfig(
    level=logging.INFO,
    filemode="w",
    format="%(levelname)s %(message)s",
)


class ServerQuery:
    def __init__(self):
        self.server_status_tracker = {}

    def query(self, server_endpoint):
        logging.info(f"querying {server_endpoint}...")
        response = requests.get(server_endpoint)
        application_name = response.json().get("Application")
        logging.info(f"Application: {application_name}")
        application_version = response.json().get("Version")
        logging.info(f"Version: {application_version}")
        application_uptime = response.json().get("Uptime")
        logging.info(f"Uptime: {application_uptime}")
        request_count = response.json().get("Request_Count")
        success_count = response.json().get("Success_Count")
        success_rate = round(float(success_count / request_count), 5)
        logging.info(
            f"Success rate for {application_name} (v{application_version}): {success_rate} \n"
        )

        return application_name, application_version, success_rate

    def output(self, application, version, success_rate):
        if self.server_status_tracker.get(application):
            application_name = self.server_status_tracker[application]
            if version in application_name["Versions"].keys():
                success_rates = application_name["Versions"][version][
                    "success_rates"
                ]
                success_rates.append(success_rate)
                application_name["Versions"].update(
                    {
                        version: {
                            "success_rates": success_rates,
                            "average_success_rate": sum(success_rates)
                            / len(success_rates),
                        }
                    }
                )
            else:
                application_name["Versions"].update(
                    {
                        version: {
                            "success_rates": [success_rate],
                            "average_success_rate": success_rate,
                        }
                    }
                )
        else:
            self.server_status_tracker.update(
                {
                    application: {
                        "Versions": {
                            version: {
                                "success_rates": [success_rate],
                                "average_success_rate": success_rate,
                            },
                        }
                    }
                }
            )

        return self.server_status_tracker

    def main(self, file_name):
        with open(file_name, "r") as file:
            for line in file.readlines():
                line = line.rstrip().lstrip()
                application, version, success_rate = self.query(
                    server_endpoint=line
                )
                self.output(
                    application=application,
                    version=version,
                    success_rate=success_rate,
                )

        return self.server_status_tracker
