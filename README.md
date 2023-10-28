https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true

This scraper can be executed by running the file 'nevadaepro.py'

* It extracts the following fileds.
    o	Bid Solicitation # 
    o	Buyer
    o	Description
    o	Bid Opening Date

    sample data
    {
            "Bid Solicitation #": "80DOT-S2558",
            "Buyer": "Joel Smedes",
            "Description": "EZ Series 1500 Melter",
            "Bid Opening Date": "11/17/2023 14:00:00"
}

*   The extracted json stored in the dir Pages as page numbers i json format.
    all header information extracted by individual bid soliciation number stored in dir Bid_numbers in respective dir named by the bi numbers

    sample data
    {
        "Bid Number:": "01GO-S2521",
        "Description:": "Independent Verification and Validation (IV&V) Services",
        "Bid Opening Date:": "11/01/2023 02:00:00 PM",
        "Purchaser:": "Joel Smedes",
        "Organization:": "Governor's Office",
        "Department:": "015 - Governor's Finance Office",
        "Location:": "1325 - Office of Project Management",
        "Fiscal Year:": "24",
        "Type Code:": "",
        "Allow Electronic Quote:": "Yes",
        "Alternate Id:": "",
        "Required Date:": "",
        "Available Date:": "10/03/2023 03:25:57 PM",
        "Info Contact:": "Joel Smedes; 775-684-0172; j.smedes@admin.nv.gov",
        "Bid Type:": "OPEN",
        "Informal Bid Flag:": "Open Market",
        "Purchase Method:": "This is a formal RFP request seeking qualified vendors to provide a comprehensive evaluation of the CORE.NV project implementation for the Governor's Finance Office, Office of Project Management . Please see the RFP and the Scope of Work in the 'Attachments' tab for specification information.",
        "Pre Bid Conference:": "Office of Project Management3850 Arrowhead DriveGovernor's Finance OfficeOffice of the GovernorState of NevadaCarson City,NV 89706USEmail: ASDAPGroup@admin.nv.govPhone: (775)687-7220Alt. Reference: 070",
        "Bulletin Desc:": "Bill To: Administrative Services Division209 E Musser St Rm 304Administrative Services DivisionDepartment of AdministrationState of NevadaCarson City,NV 89701USEmail: ASDAPGroup@admin.nv.govPhone: (775)684-0273Alt. Reference: 002",
        "Ship-to Address:": "",
        "Bill-to Address:": "1"
}

 * By navigating to the individual bid soliciation number urls, it downloads the attachments stored in the respective folder of the bid number.

* Pagination is set to False. pagn param is set to False by default, it can be changed to True to scrape pagination.




