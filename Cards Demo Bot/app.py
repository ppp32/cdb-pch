from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
from cardcontent import *
import smartsheet

app = Flask(__name__)
api = WebexTeamsAPI(access_token="ZWU5ZjdhNjctZDM4YS00MGVmLThjMWEtMTJkNTMwMWE1NjNiN2EwNzk2MTItMWQy_PE93_2dc7171a-e3cc-4b0b-8046-94a26d37b60b")

@app.route('/', methods=['POST', 'GET'])
def home():
    return 'OK',200

@app.route('/webhookreq', methods=['POST', 'GET'])
def webhookreq():
    if request.method == 'POST':
        req = request.get_json()
        data_personId = req['data']['personId']
        data_roomId = req['data']['roomId']
        #Loop prevention VERY IMPORTNAT!
        me = api.people.me()
        if data_personId == me.id:
            return 'OK ME ID', 200
        else:
            if api.messages.create(roomId=data_roomId, text='Hello Woooorld!!!', attachments=[{"contentType":"application/vnd.microsoft.card.adaptive", "content": cardcontent}]):
                return "OK OK"
    elif request.method == 'GET':
        return "Yes, this is working."
    return 'OK END', 200

@app.route('/cardsubmitted', methods=['POST'])
def cardsubmitted():
    if request.method == 'POST':
        req = request.get_json()

        data_id = req['data']['id']

        attachment_actions = api.attachment_actions.get(data_id)
        inputs = attachment_actions.inputs

        myName = inputs['myName']
        myEmail = inputs['myEmail']
        myTel = inputs['myTel']

        print(myName)
        print(myEmail)
        print(myTel)

        smart = smartsheet.Smartsheet('FjC98fH7sIKCiydVfAvIQW0rtvboSNi1zX0z5') #Smartsheet Access Token
        smart.errors_as_exceptions(True)

        # Specify cell values for the added row                         
        newRow = smartsheet.models.Row()
        newRow.to_top = True
      # The above variables are the incoming JSON
        newRow.cells.append({ 'column_id': 2646682889414532, 'value': myName })                   #  
        newRow.cells.append({ 'column_id': 7150282516785028, 'value': myEmail, 'strict': False })   
        newRow.cells.append({ 'column_id': 1520782982571908, 'value': myTel, 'strict': False }) 
        response = smart.Sheets.add_rows(7050997496342404, newRow) 


    return 'OK', 200

if __name__=='__main__':
    app.debug = True
    app.run(host="0.0.0.0")