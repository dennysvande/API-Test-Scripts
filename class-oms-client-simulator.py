import random
import json
import time
import pandas as pd
import requests

class ClientSimulator:
    def __init__(self):
        self.timestr = time.strftime("%Y%m%d-%H%M%S")   # set the time of simulator is running
        self.file_path = "oms-fat-test-" + self.timestr + ".log"    # set file path for the log
        self.customers_data = pd.read_csv("fantasy-island-customers.txt", sep='\t') # read customers data
        #self.crews_data = pd.read_csv("fantasy-island-crews.csv")  # read crews data
        self.crews_data = pd.read_csv("fantasy-island-crewsEmployees.txt", sep='\t')    # read crews data
        self.incidents_data = pd.read_csv("list-of-incidents-second.csv")   # read incidents data
        self.all_switches = pd.read_csv("all-switches.csv") # read device(switches) data
        self.all_switches_unique = self.all_switches["ID"][18:1128].unique()
        self.outage_id = pd.read_csv("created-planned-outage.csv")

    def FormatResponse(self, response):
        str_response = response.content.decode('utf8')  # decode the content from utf to raw JSON string
        json_response = json.loads(str_response)        # parse JSON and convert to python dict() object
        formatted_response = json.dumps(json_response, indent=4, sort_keys=False) # indent the dict() object and convert it back to JSON
        return formatted_response

    def WriteResponseFile(self, response, index):
        with open(self.file_path, 'a') as file:     # open file on the path define in the class constructor (__init__)
            file.write(str(index) + '\n')           # prepend it with index to keep track the number of response
            file.write(response)                    # append the response to the end of file
            file.write('\r\n')

class AMI(ClientSimulator):
    def Reading(self):
        url = "http://192.168.42.140:8443/api/adms/ami/v2/reading"  
        print("Start test")
        start_test_time = time.time()

        for index in range(1, 1001):
            payload_data = {
                "RequestId": "",
                "MeterId": "",
                "VoltA": "2",
                "VoltB": "3",
                "VoltC": "4",
                "VarA": "5",
                "VarB": "6",
                "VarC": "7",
                "WattA": "8",
                "WattB": "9",
                "WattC": "10",
                "AmpA": "11",
                "AmpB": "12",
                "AmpC": "13",
                "LastCommunicationTime": ""
            }

            response = requests.post(url, json=payload_data, timeout=10)
            formatted_response = self.FormatResponse(response)
            self.WriteResponseFile(formatted_response, index)
            if (time.time() - start_test_time) >= 60:
                print("Time elapsed: ", time.time() - start_test_time)
                break

    def Event(self):
        url = "http://192.168.142.140:8443/api/adms/ami/v2/event"
        print("Start test")
        start_test_time = time.time()

        for index in range(1, 1001):
            payload_data = {
                "MeterId": "312304KT",
                "Event": "PowerOut",
                "EventCode": 0
            }

            response = requests.post(url, json=payload_data, timeout=10)
            formatted_response = self.FormatResponse(response)
            self.WriteResponseFile(formatted_response, index)
            if (time.time() - start_test_time) >= 60:
                print("Time elapsed: ", time.time() - start_test_time)
                break

    def VoltEvent(self):
        url = "http://192.168.42.140:8443/api/adms/ami/v2/voltEvent"    # define URL for sending a VoltEvent message to ADMS
        print("Start test")
        start_test_time = time.time()                                   # start tracking the time of testing

        for index in range(1, 1001):                                    # loop into array of 1000 unique customers account numbers
            payload_data = {                                            # crafting the VoltEvent payload
                "RequestId": "",
                "MeterId": self.customers_data["METERNUMBER"][index],   # retrieve account number of each customer from the array
                "VoltA": "2",
                "VoltB": "3",
                "VoltC": "4",
                "VarA": "5",
                "VarB": "6",
                "VarC": "7",
                "WattA": "8",
                "WattB": "9",
                "WattC": "10",
                "AmpA": "11",
                "AmpB": "12",
                "AmpC": "13",
                "TimeReported": ""
            }

            response = requests.post(url, json=payload_data, timeout=10) # send a VoltEvent request to ADMS
            formatted_response = self.FormatResponse(response)           # format the response received from ADMS to be readable
            self.WriteResponseFile(formatted_response, index)            # write the formatted response to a log file
            if (time.time() - start_test_time) >= 60:                    # check if the time of testing has passed 60 seconds mark
                print("Time elapsed: ", time.time() - start_test_time)
                break                                                    # stop sending request and tracking time of testing

class Call(ClientSimulator):
    def CallsPost(self):
        url = "http://192.168.42.140:8443/api/adms/call/v2/Calls"   # define the url for create call message
        print("Start test")
        start_test_time = time.time()                               # start tracking the time of testing

        for index in range(1, 1501):                                # loop into array of 1500 unique customers and create a call for each one

            payload_data = [                                        # crafting the payload for create call
                {
                    "Name": self.customers_data["CUSTOMERNAME"][index], # retrieve each customer name from the array
                    "AccoundId": str(self.customers_data["ACCOUNTNUMBER"][index]),  # retrieve each customer account number from the array
                    "CallType": random.randint(1, 16)                   # generate a random calltype for each customer
                }
            ]

            response = requests.post(url, json=payload_data, timeout=10)    # send the request to ADMS interface
            formatted_response = self.FormatResponse(response)  # format the response received from ADMS to be readable
            self.WriteResponseFile(formatted_response, index)   # write the formatted response to a log file
            time.sleep(2)                                       # wait for 2 seconds

        end_test_time = time.time()                             # stop tracking the time of testing
        print("End test")
        print("Time elapsed: ", end_test_time - start_test_time)

class Crew(ClientSimulator):
    def UpdateCrewStatus(self):
        url = "http://192.168.42.140:8443/api/adms/crew/v2/UpdateCrewStatus"    # define the URL for updating the status of the crew
        print("Start test")
        start_test_time = time.time()                                           # start tracking the time of testing

        for index in range(1000):                                               # updating the status of crew 1000 times
            payload_data = {                                                    # crafting the payload for updateing crew status
                "CrewId": self.crews_data['Id'][index],                         # retrieve each crew data from the array
                "WorkStatus": random.randint(1, 5),                             # generate random work status for each crew
                "AvailabilityStatus": 2,                                        # set availability status for each crew
                "ShiftStatus": random.randint(1, 4)                             # generate random shift status for each crew
            }

            response = requests.post(url, json=payload_data, timeout=10)        # send the request with the payload to ADMS
            formatted_response = self.FormatResponse(response)                  # format the response received from ADMS to be readable
            self.WriteResponseFile(formatted_response, index)                   # write the formatted response to a log file
            time.sleep(5)                                                       # wait for 5 seconds

        end_test_time = time.time()                                             # stop tracking the time of testing                                             
        print("End test")
        print("Time elapsed: ", end_test_time - start_test_time)

    def UpdateIncident(self):
        url = "http://192.168.42.140:8443/api/adms/crew/v2/UpdateIncident"
        print("Start test")
        start_test_time = time.time()

        for index in range(1000):
            payload_data = {
                "IncidentId": self.incidents_data["Incident #"][index],
                "Comment": ""
            }

            response = requests.post(url, json=payload_data, timeout=10)
            formatted_response = self.FormatResponse(response)
            self.WriteResponseFile(formatted_response, index)
            time.sleep(5)

        end_test_time = time.time()
        print("End test")
        print("Time elapsed: ", end_test_time - start_test_time)

    def addEmployee(self):
        url = "http://172.30.1.13:8443/api/adms/crew/model/v2/addEmployee"
        data = [
            {
                "EmployeeId":"FI1407",
                "FirstName":"Elliot",
                "LastName":"Alderson",
                "CrewDivision":"DispatchNorth",
                "EmployeeTypeName":"Local Lineman",
                "CrewArea":"3Lions District Crews",
                "DefaultCrewArea":"3Lions District Crews",
            }
        ]

        response = requests.post(url, json=data, timeout=10)
        print(self.FormatResponse(response))

    def updateEmployee(self):
        url = "http://172.30.1.13:8443/api/adms/crew/model/v2/updateEmployee"
        data = [
            {
                "EmployeeId":"FI1407",
                "Updates":[
                    {
                        "PropertyName":"Dept",
                        "Value":"Dist Ops"
                    },
                    {
                        "PropertyName":"CanSwitch",
                        "Value":True
                    },
                    {
                        "PropertyName":"RadioNumber",
                        "Value":"4343"
                    }
                ]
            }
        ]

        response = requests.post(url, json=data, timeout=10)
        print(self.FormatResponse(response))

    def deleteEmployee(self):
        url = "http://172.30.1.13:8443/api/adms/crew/model/v2/deleteEmployee"
        data = [
            {
                "EmployeeId":"FI1407"
            }
        ]

        response = requests.post(url, json=data, timeout=10)
        print(self.FormatResponse(response))

class Incident(ClientSimulator):
    def GetIncidentByName(self):
        url = "http://192.168.42.140:8802/oms/services/rest/GetIncidentByName?incidentName="    # define the URL to query incident details
        print("Start test")
        start_test_time = time.time()                           # start tracking the time of testing

        for index in range(1, 1501):                            # loop into array of 1500 unique incidents and query details for each one
            response = requests.get(url + str(int(self.incidents_data["Incident #"][index])), timeout=10)   # send incident query request to ADMS for each incident

            formatted_response = self.FormatResponse(response)  # format the response received from ADMS to be readable
            self.WriteResponseFile(formatted_response, index)   # write the formatted response to a log file
            time.sleep(2)                                       # wait for 2 seconds

        end_test_time = time.time()                             # stop tracking the time of testing
        print("End test")
        print("Time elapsed: ", end_test_time - start_test_time)

class Outage(ClientSimulator):
    def CreatePlannedOutage(self):
        url = "http://192.168.42.140:8802/oms/services/rest/CreatePlannedOutage"    # define URL for creating a planned outage
        print("Start test")
        start_test_time = time.time()   # start tracking the time of testing

        for index in range(1, 2001):    # loop into array of 2000 unique switches (devices) to create a planned outage for each one
            payload_data = {            # crafting create planned outage payload
                "PlannedOutageRecord": {
                    "AlternateEndTimeBinary": "/Date(1705010400000)/",
                    "AlternateStartTimeBinary": "/Date(1705006800000)/",
                    "CausesIncident": True,
                    "CustomerAccountsNotify": [
                        {
                            "CustomerKey": "",
                            "Notify": True
                        }
                    ],
                    "DeviceId": str(self.all_switches["ID"][index]),    # retrieve each switch data from the array 
                    "EventType": "2",
                    "OutageMessage": "Created PO via OIS",
                    "PlannedOutageType": "1",
                    "PrimaryEndTimeBinary": "/Date(1704924000000)/",
                    "PrimaryStartTimeBinary": "/Date(1704920400000)/",
                    "RepresentativeAddress": "test1",
                    "RepresentativeEmail": "test2",
                    "RepresentativeName": "test3",
                    "RepresentativeNumber": "test4",
                    "Station": "RAVEN",
                    "UseAlternateDate": False,
                    "CustomFields": [
                        {
                            "PropertyName": "PO1",
                            "Value": "true"
                        },
                        {
                            "PropertyName": "PO2",
                            "Value": "1"
                        },
                        {
                            "PropertyName": "PO3",
                            "Value": "TEST CUSTOM FIELDS - from OIS"
                        },
                        {
                            "PropertyName": "PO4",
                            "Value": "123000"
                        },
                        {
                            "PropertyName": "PO5",
                            "Value": "05/12/2021 12:30 PM"
                        },
                        {
                            "PropertyName": "PO6",
                            "Value": "Additional Custom Fields - not configured"
                        }
                    ]
                },
                "authorName": "DMSALL"
            }

            response = requests.post(url, json=payload_data, timeout=10)    # send the create planned outage request to ADMS
            formatted_response = self.FormatResponse(response)              # format the resposne to be readable
            self.WriteResponseFile(formatted_response, index)
            time.sleep(3.6)                                                 # wait for 3.6 seconds

        end_test_time = time.time()                                         # stop tracking the time of testing
        print("End test")
        print("Time elapsed: ", end_test_time - start_test_time)

    def UpdatePlannedOutage(self):
        url = "http://192.168.42.140:8802/oms/services/rest/UpdatePlannedOutage"
        print("Start test")
        start_test_time = time.time()

        for index in range(1, 2001):
            payload_data = {
                "Fields": [
                    {
                        "PropertyName": "Status",
                        "Value": 1
                    }
                ],
                "PlannedOutageId": str("00" + str(self.outage_id["Outage ID"][index])),
                "userName": "DMSALL"
            }

            response = requests.post(url, json=payload_data, timeout=10)
            formatted_response = self.FormatResponse(response)
            self.WriteResponseFile(formatted_response, index)
            #time.sleep(3.6)

        end_test_time = time.time()
        print("End test")
        print("Time elapsed: ", end_test_time - start_test_time)

    def DeletePlannedOutage(self):
        url = "http://192.168.42.140:8802/oms/services/rest/DeletePlannedOutage"
        print("Start test")
        start_test_time = time.time()

        for index in range(1, 2001):
            payload_data = {
                "PlannedOutageId": str("00" + str(self.outage_id["Outage ID"][index])),
                "userName": "DMSALL"
            }

            response = requests.post(url, json=payload_data, timeout=10)
            formatted_response = self.FormatResponse(response)
            self.WriteResponseFile(formatted_response, index)
            #time.sleep(3.6)

        end_test_time = time.time()
        print("End test")
        print("Time elapsed: ", end_test_time - start_test_time)

    def ViewOutagePortal(self):
        url = "http://192.168.42.140:8801/dms/services/SwitchStatus"
        print("Start test")
        start_test_time = time.time()
        #print(len(self.all_switches_unique))

        for index, data in enumerate(self.all_switches_unique):
            payload_data = {
                "StationName": "3LIONS",
                "SwitchId": data,
                "Status": True
            }

            #print(index, data, type(data))
            #print(self.all_switches["Address"][index].split(" ")[3])

            response = requests.post(url, json=payload_data, timeout=10)
            self.WriteResponseFile(response.text, index)
            time.sleep(3.6)

        end_test_time = time.time()
        print("End test")
        print("Time elapsed: ", end_test_time - start_test_time)

if __name__ == "__main__":

    #ami_client = AMI()
    #ami_client.VoltEvent()
    #retrieve_incident = Incident()
    #retrieve_incident.GetIncidentByName()
    #crew_client = Crew()
    #crew_client.UpdateCrewStatus()
    call_client = Call()
    call_client.CallsPost()
    #outage_client = Outage()
    #outage_client.CreatePlannedOutage()
    #outage_client.ViewOutagePortal()
    #outage_client.UpdatePlannedOutage()
    #outage_client.DeletePlannedOutage()
