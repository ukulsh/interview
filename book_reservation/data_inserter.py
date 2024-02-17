import requests

books = """1000,Book 1,2
1001,Book 2,4
1002,Book 3,1
1003,Book 4,3
1004,Book 5,1
1005,Book 6,2
1006,Book 7,4
1007,Book 8,4
1008,Book 9,3
1009,Book 10,1
1010,Book 11,5
1011,Book 12,5
1012,Book 13,4
1013,Book 14,3
1014,Book 15,3
1015,Book 16,5
1016,Book 17,4
1017,Book 18,1
1018,Book 19,4
1019,Book 20,5"""

for book in books.split("\n"):
    id, name, number_of_copies = book.split(',')
    id = int(id)
    number_of_copies = int(number_of_copies)
    payload = {
        "id": id,
        "name": name,
        "number_of_copies": number_of_copies
    }
    requests.post(data=payload, url='http://localhost:8000/book/', verify=False)

members = """2000,Member 1
2001,Member 2
2002,Member 3
2003,Member 4
2004,Member 5
2005,Member 6
2006,Member 7
2007,Member 8
2008,Member 9
2009,Member 10
2010,Member 11
2011,Member 12
2012,Member 13
2013,Member 14
2014,Member 15
2015,Member 16
2016,Member 17
2017,Member 18
2018,Member 19
2019,Member 20"""

for member in members.split('\n'):
    id, name = member.split(',')
    id = int(id)
    payload = {
        'id': id,
        'name': name
    }
    requests.post(data=payload, url='http://localhost:8000/member/', verify=False)
