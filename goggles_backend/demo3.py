from havenondemand.hodclient import *

hodClient = HODClient("f148d587-dfd9-4edd-ba32-14b81659f40b", "v1")
_CONNECTOR = 'sfgov19'

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

    #update_connector()
    create_connector()
    start_connector()
    connector_status()
    #stop_connector()