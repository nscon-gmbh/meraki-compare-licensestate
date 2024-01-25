# meraki-compare-licensestate

get license volume for Co-Termination Licensing model via api and compare to last state. Save result in a CSV file and send it via Mail.
 
## Use Case Description

For Co-Termination Licensing it is not possible to get the current used licenses via API. For this reason, we have developed a solution to capture a list of all active devices, assigned to a network and print this to a .csv file.


## Installation

Use a virtual environment and install the missing python packages using the command

1. Clone the repository and change into new directory:

```bash
git clone https://github.com/nscon-gmbh/meraki-quick-check.git
cd meraki-quick-check
```

2. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python modules used in the script:
 
```bash
pip install -r requirements.txt
```

## Configuration

Please enter the following information into the file .env in the local directory.

```
APIKEY=\<your Meraki API Key\>
ORGID=\<Meraki Org ID for which you want to capture the data\>
CLIENTID=\<MS Graph ClientID\>
CLIENTSECRET=\<MS Graph ClientSecret\>
TENANTID=\<MS Graph TenantID\>
FROM=\<mail sender, you need to have the necessary rights to send a mail from this mail address\>
TO=\<mail receiver - for multiple receiver seperate the strings with a , -\> receiver@1.com,receiver@2.com\>
CC=\<mail CC - for multiple receiver seperate the strings with a , -\> receiver@1.com,receiver@2.com\>
```
## Usage

`python main.py`

CSV Result will be similar to:
```csv
product;2023_12_01; 2024_01_01; difference; 
MR62;1;1; 0;
MR33;10;5; -5;
MR56;5;5; 0;
MR46;8;8; 0;
MR36;2;; 0;
MR76;1;1; 0;
MS355-24X2;3;3; 0;
MS425-16;2;2; 0;
MS425-32;2;2; 0;
MS225-24P;10;8; -2;
MS225-48LP;9;9; 0;
MS250-24P;16;22; 6;
MS250-48LP;7;7; 0;
MS250-48FP;4;4; 0;
MS120-8;1;5; 4;
MX67;1;1; 0;
MX67C-WW;76;77; 1;
MX68;6;6; 0;
MX68CW-WW;0;0; 0;
MX250;1;1; 0;
MX105;1;5; 4;
MX85;0;0; 0;
MG41E;3;3; 0;
```

### DevNet Sandbox

This script was tested with the [Cisco DevNet Meraki Always On sandbox](https://devnetsandbox.cisco.com/DevNet). Please double check that the API key provided in the instructions is a valid one and present in the profile of the sandbox user before using it.

## How to test the software

The repo is instrumented with a continuous testing framework.

## Known issues

Functionality is limited to Co-Termination Licensing.

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository or get in contact with the author.

## Getting involved

Please get involved by giving feedback on features, fixing certain bugs, building important pieces, etc.

## Author(s)

This project was written and is maintained by the following individuals:

* Sebastian Otto <s.otto@nscon.de>
