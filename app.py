from flask import Flask,request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse


#instantiatin Flask
app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])
#defining the main function for the bot
def botnet():
    msg = request.form.get('Body').lower()
    resp = MessagingResponse()

    

    #list for storing data

    covid_list =[]
    covid_info = []

    covid_session =False

    if msg == 'hi':
        resp.message("Hi, I am your medical assistant \n Please select any of the following \n 1.Covid Information \n 2. Disease knowledge base")
        return str(resp)

    if msg == '1':
        url = 'https://covid19.mathdro.id/api'
        resp.message('Getting global stats')
        resp.message('To get specific results for a country type covid then the country \n e.g covid Zimbabwe')
        

        response = requests.request("GET",url)

        data = json.loads(response.text)

        confirmed_cases = 'Total Global Cases : ' + str(data['confirmed']['value'])
        recovered = 'Total Recovered: ' + str(data['recovered']['value'])

        covid_list.append(confirmed_cases)
        covid_list.append(recovered)

        for item in covid_list:
            resp.message(item)

        return str(resp)
    

    if 'covid' in msg:
        message = msg.replace('covid', '').strip()
        url = 'https://covid19.mathdro.id/api/countries/%s' %message

        response = requests.request("GET",url)
        data = json.loads(response.text)

        resp.message('Covid19 results for : '+ message)

        conf = "Total cases : "+ str(data['confirmed']['value'])
        conf_deaths = "Total deaths : " + str(data['deaths']['value'])

        covid_info.append(conf)
        covid_info.append(conf_deaths)

        for i in covid_info:
            resp.message(i)

        return str(resp)

#logic for 2nd option
    if msg == '2':
        resp.message('Diesease knowledgebase Activated, To get information about a diesease : \n 1.Use keyword *disease* eg disease malaria \n 2. To get symptoms information use keyword *symptoms* eg symptoms cholera')
    
        return str(resp)

    #creating an option"function" for when the user searches a certain disease
    if 'disease' in msg:

        #list
        data_list = []
        message = msg.replace('disease','').strip()

        url = 'https://disease-info-api.herokuapp.com/diseases/%s' %message
        result = requests.request("GET",url)

        data = json.loads(result.text)

        explanation = str(data['disease']['facts'])

        data_list.append(explanation)

        resp.message(str(data_list)[3:-3])
        
        return str(resp)   

    if 'symptoms' in msg:
        symptoms_list = []
        message = msg.replace('symptoms','').strip()

        url = 'https://disease-info-api.herokuapp.com/diseases/%s' %message
        result = requests.request("GET",url)

        data = json.loads(result.text)

        explanation = str(data['disease']['symptoms'])

        symptoms_list.append(explanation)

        resp.message(str(symptoms_list)[18:-1])
        
        return str(resp) 


if __name__ == '__main__':
    app.run()
