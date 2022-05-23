import logging, requests, sys

logging.basicConfig(
    level=logging.INFO,
    filemode="w",
    format="%(levelname)s %(message)s",
)


class ServerQuery:
    def __init__(self):
        self.server_status_tracker = {}

    def query(self, server_endpoint):
        """
        This method queries a given server endpoint through an http request
        Parameters:
        -----------
        server_endpoint: str
            a server_name or url

        Returns:
        --------
        application_name: str
            the application name in response
        application_version: str
            the version of the application
        success_rate: float
            the number of successful requests per request count
        """
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
        """
        This method generates a dictionary output with information perataining to each application
        at a version and success rate level
        Parameters:
        -----------
        application_name: str
            the application name in response
        application_version: str
            the version of the application
        success_rate: float
            the number of successful requests per request count

        Returns:
        --------
        server_status_tracker: dict
            dictionary with information on each application with versions and success rates
        """

        if self.server_status_tracker.get(application):
            application_name = self.server_status_tracker[application]

            # Check if this version of application is already entered
            if version in application_name["Versions"].keys():
                success_rates = application_name["Versions"][version][
                    "success_rates"
                ]

                # Append the success rate to the list of success rates for this version and
                # update the application with new version info
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
                # Just update application with new version info
                application_name["Versions"].update(
                    {
                        version: {
                            "success_rates": [success_rate],
                            "average_success_rate": success_rate,
                        }
                    }
                )
        else:
            # Create a new application key
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

    def main(self, file_path):
        """
        This method generates a dictionary output with information perataining to each application
        at a version and success rate level
        Parameters:
        -----------
        file_path: str
            path to txt file containing servers

        Returns:
        --------
        server_status_tracker: dict
            dictionary with information on each application with versions and success rates
        """
        with open(file_path, "r") as file:
            for line in file.readlines():
                line = line.rstrip().lstrip()
                # We want to capture and handle exceptions and continue querying other endpoints
                try:
                    application, version, success_rate = self.query(
                        server_endpoint=line
                    )
                except Exception:
                    error_type = sys.exc_info()[0]
                    logging.error(
                        f"The endpoint: {line} could not be reached because of the following reason {error_type.__name__} \n"
                    )
                self.output(
                    application=application,
                    version=version,
                    success_rate=success_rate,
                )

        return self.server_status_tracker
