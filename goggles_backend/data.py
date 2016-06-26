from havenondemand.hodclient import *

hodClient = HODClient("f148d587-dfd9-4edd-ba32-14b81659f40b", "v1")

# callback function
def requestCompleted(response, error, **context):
    text = ""
    if error is not None:
        for err in error.errors:
            if err.error == ErrorCode.QUEUED or err.error == ErrorCode.IN_PROGRESS:
                # wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
                print (err.reason)
                time.sleep(5)
                hodClient.get_job_status(err.jobID, requestCompleted)
            else:
                text += "Error code: %d \nReason: %s \nDetails: %s\n" % (err.error,err.reason, err.detail)
    elif response is not None:
        text = response;
    print (text)

def asyncRequestCompleted(jobID, error, **context):
    if error is not None:
        for err in error.errors:
            if err.error == ErrorCode.QUEUED or err.error == ErrorCode.IN_PROGRESS:
                print (err.reason)
                time.sleep(2)
                hodClient.get_job_status(err.jobID, requestCompleted, **context)
            else:
                print ("Error code: %d \nReason: %s \nDetails: %s\n" % (err.error,err.reason, err.detail))
    elif jobID is not None:
        hodClient.get_job_status(jobID, requestCompleted, **context)

#data0 = [["", "", "", "", ""]];

data = [["Lobbyist Activit Contacts of Public Officials",
         "https://data.sfgov.org/api/views/hr5m-xnxc/rows.csv?accessType=DOWNLOAD",
         "https://data.sfgov.org/City-Management-and-Ethics/Lobbyist-Activity-Contacts-of-Public-Officials/hr5m-xnxc",
         "publicmeetings2",
         "Open Data, SF Board of Ethics, SF Board of Supervisors, Lobbyists, Public Officials"
         "text"],
        ["Campaign Finance FPPC Form 460 Schedule A",
         "https://data.sfgov.org/api/views/4tts-fyix/rows.csv?accessType=DOWNLOAD",
         "https://data.sfgov.org/City-Management-and-Ethics/Campaign-Finance-FPPC-Form-460-Schedule-A-Monetary/q66q-d2tr",
         "publicmeetings2",
         "Open Data, SF Board of Supervisors, Campaign, Finance"
         "text"],
        [
         "Campaign Finance San Francisco Committee",
         "https://data.sfgov.org/api/views/t7mf-3ftv/rows.csv?accessType=DOWNLOAD",
         "https://data.sfgov.org/City-Management-and-Ethics/Campaign-Finance-San-Francisco-Campaign-Committees/t7mf-3ftv",
         "publicmeetings2",
         "Open Data, SF Board of Supervisors, Campaign, Finance"
         "text"],
        [
         "BOS Full Board Of Supervisors",
         "http://sanfrancisco.granicus.com/TranscriptViewer.php?view_id=10%26clip_id=25246",
         "http%3A%2F%2Fsanfrancisco.granicus.com%2FMediaPlayer.php%3Fview_id%3D10%26clip_id%3D2437",
         "publicmeetings2",
         "Meeting Minutes, SF Board of Supervisors, City, San Francisco"
         "video"]
        ];


#
# data[0][0] = "https://data.sfgov.org/api/views/hr5m-xnxc/rows.csv?accessType=DOWNLOAD"
# data[0][1] = "https://data.sfgov.org/City-Management-and-Ethics/Lobbyist-Activity-Contacts-of-Public-Officials/hr5m-xnxc"
# data[0][2] = "publicmeetings2"
# data[0][3] = "Open Data, SF Board of Ethics, SF Board of Supervisors, Lobbyists, Public Officials"


# data[0].append("https://data.sfgov.org/City-Management-and-Ethics/Lobbyist-Activity-Contacts-of-Public-Officials/hr5m-xnxc")
# data[0].append("publicmeetings2"),
# data[0].append("Open Data, SF Board of Ethics, SF Board of Supervisors, Lobbyists, Public Officials")

#data.append(["hi", "romil", "index", "meta"]);


def create_all_records():
    for row in range(len(data)):
        print(create_text_data(data[row][0], data[row][1], data[row][2], data[row][3],data[row][4], data[row][5] ));


def create_text_data(title, url, url2, index, metadata, mytype):
    paramArr = {}
    paramArr["url"] = url
    paramArr["index"] = index
    paramArr["duplicate_mode"] = "replace"
    paramArr["additional_metadata"] = "{ \"url\": \"%s\", \"metadata\": \"%s\", \"heading\": \"%s\" , \"type\": \"%s\"}" % (url2, metadata, title, mytype)

    hodClient.get_request(paramArr, HODApps.ADD_TO_TEXT_INDEX, async=False, callback=requestCompleted)




def create_connector():
    paramArr = {}
    paramArr["flavor"] = "web_cloud"
    paramArr["connector"] = _CONNECTOR
    paramArr["config"] = """{
        "url": "http://sanfrancisco.granicus.com/ViewPublisher.php?view_id=10",
        "depth": 0
    }"""
    paramArr["destination"] = """
    {
        "action": "addtotextindex",
        "index": "publicmeetings2"
    }"""
    hodClient.get_request(paramArr, HODApps.CREATE_CONNECTOR, async=False, callback=requestCompleted)

def update_connector():
    paramArr = {}
    paramArr["connector"] = _CONNECTOR
    paramArr["config"] = """{
        "url": "https://data.sfgov.org/Economy-and-Community",
        "depth": 0,
        "clip_page": "true",
        "clip_page_using_css_select": "a.browse2-result-name-link",
        "clip_page_using_css_unselect": "div.banner,div.header,div.footer"
    }"""
    paramArr["destination"] = """
    {
        "action": "addtotextindex",
        "index": "publicmeetings3"
    }"""
    hodClient.get_request(paramArr, HODApps.UPDATE_CONNECTOR, async=False, callback=requestCompleted)


def start_connector():
    paramArr = {}
    paramArr["connector"] = _CONNECTOR
    paramArr["destination"] = """
    {
        "action": "addtotextindex",
        "index": "publicmeetings2"
    }"""
    hodClient.get_request(paramArr, HODApps.START_CONNECTOR, async=False, callback=requestCompleted)


def stop_connector():
    paramArr = {}
    paramArr["connector"] = _CONNECTOR
    hodClient.get_request(paramArr, HODApps.STOP_CONNECTOR, async=False, callback=requestCompleted)


def connector_status():
    paramArr = {}
    paramArr["connector"] = _CONNECTOR
    hodClient.get_request(paramArr, HODApps.CONNECTOR_STATUS, async=False, callback=requestCompleted)

if __name__ == "__main__":
    create_all_records()
    #update_connector()
    #create_connector()
    #start_connector()
    #connector_status()
    #stop_connector()