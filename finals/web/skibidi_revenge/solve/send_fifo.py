import requests

r = requests.get('http://localhost:5000/upload', params= {'tar': 'H4sIAOdvd2gC/+3OuQ2AQAwEwCuFEsznq4cWeCTK50RKDBLSTLLWJuuzvC+ajLgznnnf/RzjnFnrVFufQ2Tp8oPfyrHty9omCwAAAAAAAAAAAPzHBROiM7UAKAAA'})
print(r.text)