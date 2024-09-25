"""module to sync files with sharepoint site"""

from O365 import Account
from decouple import config


class _sharepoint:
    def __init__(self) -> None:
        client_id = config("CLIENTID")
        client_secret = config("CLIENTSECRET")
        tenant_id = config("TENANTID")
        account = self._authenticate(client_id, client_secret, tenant_id)
        self.storage = account.storage()

    def _authenticate(self, client_id: str, client_secret: str, tenant_id: str):
        """authenticate with Micosoft Graph API

        Args:
            client_id (str): microsoft client id
            client_secret (str): microsoft client secret
            tenant_id (str): microsoft tenant id

        Returns:
            account: O365 account object if authentication was successful
        """
        credentials = (client_id, client_secret)
        try:
            account = Account(
                credentials, auth_flow_type="credentials", tenant_id=tenant_id
            )
            if account.authenticate():
                print("Authenticated!")
            return account
        except ValueError as e:
            print(e)
            return None

    def download_file(self):
        """_summary_"""
        # File to download, and location to download to
        dl_path = "/path/to/download"
        f_name = "myfile.xlsx"

    def upload_file(self):
        """_summary_"""
        # File to upload, and location to upload to
        ul_path = "/path/to/upload"
        f_name = "myfile.xlsx"
