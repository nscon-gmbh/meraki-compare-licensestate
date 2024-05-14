""" in this script are the classes for Meraki API communication
and for creation of csv files with compare functions"""

import meraki
import csv
import glob
import pathlib
from deepdiff import DeepDiff
from datetime import datetime
from decouple import config


class _Meraki:
    def __init__(self):
        """create new dashboard api connection"""
        # get api key and orgid from .env
        api_key = config("APIKEY")
        self.org_id = config("ORGID")
        # create folder for api logs, if not existing
        folder_logs = pathlib.Path("./logs/")
        folder_logs.mkdir(parents=True, exist_ok=True)
        # initiate dashboard api connection
        self.dashboard = meraki.DashboardAPI(api_key, log_path="./logs/")

    def get_devices(self, product_types: list[str]):
        """receive all devices based on product types"""
        return self.dashboard.organizations.getOrganizationDevicesStatuses(
            self.org_id, total_pages="all", productTypes=product_types
        )

    def _get_count_devices(self, devices):
        """create list with all models of producttype"""
        list_models = []
        for device in devices:
            list_models.append(device["model"])
        dict_count_model = {i: list_models.count(i) for i in list_models}
        return dict_count_model


class _Csv:
    def write_csv_serial(self, data):
        """create new csv with provided license data"""
        self.data = data
        self.date = datetime.now().strftime("%Y_%m_%d-")
        filename = self.date + "licstate.csv"
        # create new file with license data
        try:
            with open(filename, "w") as f:
                w = csv.DictWriter(f, self.data.keys())
                w.writeheader()
                w.writerow(data)
        except Exception as e:
            print(e)

    def read_csv_reference(self):
        """read in last created csv to have base information"""
        # search for last created license .csv file
        self.csv_files = glob.glob("*licstate.csv")
        self.csv_files.sort(reverse=True)
        # read in latest .csv and return as reference data
        try:
            with open(self.csv_files[1]) as csv_file:
                csv2dict = csv.DictReader(
                    csv_file, delimiter=",", skipinitialspace=True
                )
                reference_csv_list = list(csv2dict)
                self.reference_csv = reference_csv_list[0]
        except IndexError:
            with open("reference.csv") as csv_file:
                csv2dict = csv.DictReader(
                    csv_file, delimiter=",", skipinitialspace=True
                )
                reference_csv_list = list(csv2dict)
                self.reference_csv = reference_csv_list[0]

    def write_csv_delta(self):
        """compare old and new license state and write delta to new file"""
        diffincsv = DeepDiff(self.reference_csv, self.data)
        list_of_changes = diffincsv["type_changes"]
        final_csv_name = self.date + "comparedlicenses.csv"
        # get first line of reference csv for temporary header
        csv_header_temp = self.reference_csv
        # get date from ref data
        try:
            ref_date = csv_header_temp.split("-")[0]
        except IndexError:
            ref_date = datetime.now().strftime("%Y_%m_%d")
        except AttributeError:
            ref_date = datetime.now().strftime("%Y_%m_%d")
        # current date
        time = datetime.now().strftime("%Y_%m_%d")
        # new header
        head = str("product;" + ref_date + "; " + time + "; difference; ")
        # write new header to file
        final_csv = open(final_csv_name, "w")
        final_csv.write(head)
        final_csv.close()
        try:
            # write data to new csv with delta
            for key, value in list_of_changes.items():
                product = key.split("['")[1].split("']")[0]
                delta = int(value["new_value"]) - int(value["old_value"])
                final_csv = open(final_csv_name, "a+")
                old = value["old_value"]
                new = value["new_value"]
                string = f"\n{product};{old};{new}; {delta};"
                final_csv.write(string)
                final_csv.close()
        except Exception as e:
            print(e)
        return final_csv_name
