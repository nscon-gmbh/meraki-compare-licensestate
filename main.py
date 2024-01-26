"""this script is the main script which triggers all necessary functions
to pull current list of active devices via Meraki API and compares it to
the latest information"""

from compare_license import _Meraki, _Csv
from o365 import _Mail
from decouple import config
import datetime as dt


def main():
    """this is the main function"""
    # create new dict for result
    diff_all = {}
    # list of all producttype you wish to capture the licenses for
    list_producttype = ["wireless", "switch", "appliance", "cellularGateway"]
    # create new _meraki object for API access
    dashboard = _Meraki()
    # capture licensed devices for all producttypes in list_producttype
    diff_all.update(
        **dashboard._get_count_devices(dashboard.get_devices(list_producttype))
    )
    # create new _csv object
    delta_csv = _Csv()
    # write license information to new csv
    delta_csv.write_csv_serial(diff_all)
    # read in last created csv with license information for comparison
    delta_csv.read_csv_reference()

    date = dt.date.today()
    month = date.strftime("%B")

    # instantiate new mail object
    mail = _Mail()
    mail.authenticate()
    # create header dict
    header = {}
    header["from"] = config("FROM")
    header["to"] = config("TO")
    header["cc"] = str(config("CC")).split(",")
    header["subject"] = f"license overview for the month {month}"
    # create body text
    body = f"""
    Dear receiver,
    attached you can find the license overview for the month {month}
    """
    # update created csv with delta of last created csv and attach to mail
    header["file"] = delta_csv.write_csv_delta()
    # send mail
    mail.send_mail(header, body)
    # finished
    print("data was processed.")


if __name__ == "__main__":
    main()
