from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)                       # Create the Flask application

timestr = time.strftime("%Y%m%d-%H%M%S")    # set the time of mock API server is running
file_Path = "oms.log" + timestr             # set the file path for the log containing the captured notification messages

# format the request
def format_Request(http_Request):
    str_Req = http_Request.decode('utf8')   # decode the content from utf to raw JSON string
    json_Req = json.loads(str_Req)          # parse JSON and convert to python dict() object
    formatted_Req = json.dumps(json_Req, indent=4, sort_keys=False) # indent the dict() object and convert it back to JSON
    
    return formatted_Req

def write_Request_to_File(request):
    formatted_Data = format_Request(request.data)   # format notification messages to be readable
    print(request.url)
    with open(file_Path, 'a') as file:              # open file on the path define in the global variable
        file.write(request.url + '\n')              # prepend with the request URL to track the messages
        file.write(formatted_Data)                  # write the formatted request to log file
        file.write('\r\n')
    
    return formatted_Data

# Crew Server routes (endpoints)
@app.route('/api/ext/wms/v2/ModelingStatus', methods=['POST'])
def create_Modeling_Status_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code
    
# @app.route('/api/ext/wms/v2/WMSMessages', methods=['GET'])
# def create_WMSMessages_Data():
    # # Process or retrieve the data to be returned
    # data = request.data
    # formatted_Data = format_Request(data)
    #print(formatted_Data)
    #write_Request_to_File(formatted_Data)

    # response = {'message': 'Data created successfully'}
    # return jsonify(response), 201  # 201 indicates "Created" status code
    
@app.route('/api/ext/wms/v2/IncidentUpdate', methods=['POST'])
def create_Incident_Update_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code
    
@app.route('/api/ext/wms/v2/CrewUpdate', methods=['POST'])
def create_Crew_Update_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code

@app.route('/api/ext/wms/v2/OrderUpdate', methods=['POST'])
def create_Order_Update_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code
    
@app.route('/api/ext/wms/v2/PlannedOutageUpdate', methods=['POST'])
def create_Planned_Outage_Update_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code

# @app.route('/api/ext/wms/v2/Status', methods=['POST'])
# def create_Crew_Status_Data():
    # # Process or retrieve the data to be returned
    # formatted_Data = write_Request_to_File(request)
    # print(formatted_Data)

    # response = {'message': 'Data created successfully'}
    # return jsonify(response), 201  # 201 indicates "Created" status code

# future functionality
#@app.route('/api/ext/wms/v2/WMSModelMessages', methods=['GET'])
#def create_Model_Message_Status_Data():
    # Process or retrieve the data to be returned
    #data = request.data
    #print(format_Request(data))
    #
    #response = {'message': 'Data created successfully'}
    #return jsonify(response), 201  # 201 indicates "Created" status code
    
# @app.route('/api/ext/wms/v2/ModelMessageStatus', methods=['POST'])
# def create_Model_Message_Status_Data():
    # # Process or retrieve the data to be returned
    # data = request.data
    # print(format_Request(data))

    # response = {'message': 'Data created successfully'}
    # return jsonify(response), 201  # 201 indicates "Created" status code


#########################################################################
# Call Server routes (endpoints)
@app.route('/api/ext/call/v2/CallNotification', methods=['POST'])   # define API endpoint / route and HTTP method to captured notification messages
def create_Call_Notification_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)                 # send the captured notification messages to helper function to be formatted and
    print(formatted_Data)                                           # written to a log file

    response = {'message': 'Data created successfully'}             # craft a response payload to be sent back to the client
    return jsonify(response), 201                                   # 201 indicates "Created" status code and send the response to the client
    
@app.route('/api/ext/call/v2/Callbacks', methods=['POST'])
def create_Callbacks_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code

# future functionality
# @app.route('/api/ext/call/v2/CaseNoteResponse', methods=['POST'])
# def create_Case_Note_Response_Data():
    # # Process or retrieve the data to be returned
    # data = request.data
    # print(format_Request(data))

    # response = {'message': 'Data created successfully'}
    # return jsonify(response), 201  # 201 indicates "Created" status code
    
# @app.route('/api/ext/call/v2/CaseNotes', methods=['POST'])
# def create_Case_Notes_Data():
    # # Process or retrieve the data to be returned
    # data = request.data
    # print(format_Request(data))

    # response = {'message': 'Data created successfully'}
    # return jsonify(response), 201  # 201 indicates "Created" status code

@app.route('/api/ext/call/v2/CustomerMove', methods=['POST'])
def create_Customer_Move_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code
    
@app.route('/api/ext/call/v2/CustomerResponse', methods=['POST'])
def create_Customer_Response_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code
    
# @app.route('/api/ext/call/v2/Status', methods=['POST'])
# def create_Call_Status_Data():
    # # Process or retrieve the data to be returned
    # data = request.data
    # print(format_Request(data))

    # response = {'message': 'Data created successfully'}
    # return jsonify(response), 201  # 201 indicates "Created" status code

    
#########################################################################
# AMI Server (Call Server) routes (endpoints)
@app.route('/api/ext/ami/v2/Ping', methods=['POST'])
def create_Ping_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code

@app.route('/api/ext/ami/v2/VoltPing', methods=['POST'])
def create_Volt_Ping_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code

@app.route('/api/ext/ami/v2/Control/Disconnect', methods=['POST'])
def create_Control_Disconnect_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code

@app.route('/api/ext/ami/v2/Control/Reconnect', methods=['POST'])
def create_Control_Reconnect_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code

# @app.route('/api/ext/ami/v2/Status', methods=['POST'])
# def create_AMI_Status_Data():
    # # Process or retrieve the data to be returned
    # data = request.data
    # print(format_Request(data))

    # response = {'message': 'Data created successfully'}
    # return jsonify(response), 201  # 201 indicates "Created" status code
    
#########################################################################
# Customer Experience Adapter routes (endpoints)
@app.route('/api/ext/ce/v2/PlannedOutage', methods=['POST'])    # define API endpoint / route and HTTP method to captured notification messages
def create_CXE_Planned_Outage_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)             # send the captured notification messages to helper function to be formatted and
    print(formatted_Data)                                       # written to a log file
    #print(request.data)

    response = {'message': 'Data created successfully'}         # craft a response payload to be sent back to the client
    return jsonify(response), 201                               # 201 indicates "Created" status code and send the response to the client

@app.route('/api/ext/ce/v2/IncidentUpdate', methods=['POST'])   # define API endpoint / route and HTTP method to captured notification messages
def create_CXE_Incident_Update_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)             # send the captured notification messages to helper function to be formatted and
    print(formatted_Data)                                       # written to a log file
    #print(request.data)

    response = {'message': 'Data created successfully'}         # craft a response payload to be sent back to the client
    return jsonify(response), 201                               # 201 indicates "Created" status code and send the response to the client

#########################################################################
# ANPS ViewOutagePortalNotification
@app.route('/api/ext/ANPS/v2/ViewOutagePortalNotification', methods=['POST'])
def create_View_Outage_Portal_Notification_Data():
    # Process or retrieve the data to be returned
    formatted_Data = write_Request_to_File(request)
    print(formatted_Data)

    response = {'message': 'Data created successfully'}
    return jsonify(response), 201  # 201 indicates "Created" status code

if __name__ == '__main__':
    # define the IP address and listening port
    app.run(host="0.0.0.0", port=8445, debug=True)