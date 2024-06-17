СНАЧАЛА СМЕНИ ДИРЕКТОРИЮ!!!!!
cd C:\Users\HP\Desktop\ООП   ПАПКИ ИМЕНУЙ БЕЗ ПРОБЕЛОВ!!!!!
ОБЯЗАТЕЛЬНО ПИШЕМ КОМАНДУ python
Для вызова через терминал
ДЛЯ КАЖДОГО КЛАССА ПИШЕМ
from model import название класса

>>> from model import Client
>>> c1 = Client(1,1,1,1,2,2,2,2,0)
>>> c1
Client(seniority=1,home=1,age=1,marital=1,records=2,expenses=2,amount=2,price=0)


>>> from model import KnownClient
>>> c2 = KnownClient(1,2,34,1,1,1,1,1,2,2)
>>> c2
KnownClient(seniority=2,home=34,age=1,marital=1,records=1,expenses=1,amount=2,price=2,status=1)


>>> from model import TrainingKnownClient
>>> test = TrainingKnownClient(2,2,2,2,1,1,1,1,1,0)
>>> test
TrainingKnownClient(seniority=2,home=2,age=2,marital=1,records=1,expenses=1,amount=1,price=0,status=2)


>>> from model import UnknownClient
>>> u = UnknownClient(2,2,2,2,1,1,1,1,1)
>>> u
UnknownClient(seniority=2,home=2,age=2,marital=2,records=1,expenses=1,amount=1,price=1)
>>> c = ClassifiedClient(classification = "2",client = u)
>>> c
ClassifiedClient(seniority=2,home=2,age=2,marital=2,records=1,expenses=1,amount=1,price=1,classification='2')
>>> td = TrainingData('test')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'TrainingData' is not defined
>>> from model import TrainingData
>>> td = TrainingData('test')      
>>> raw_data = [
... {"status": 10, "seniority": 17, "home": 1, "age": 58, "marital": 3, "records": 1, "expenses": 48, "assets": 2500, "amount": 
1000, "price": 1685}
... {"status": 2, "seniority": 17, "home": 1, "age": 58, "marital": 3, "records": 1, "expenses": 48, "assets": 2500, "amount": 1000, "price": 1685},
  File "<stdin>", line 2
    {"status": 10, "seniority": 17, "home": 1, "age": 58, "marital": 3, "records": 1, "expenses": 48, "assets": 2500, "amount": 
1000, "price": 1685}]
>>> td.load(raw_data)
row 1: invalid status in {'status': 10, 'seniority': 17, 'home': 1, 'age': 58, 'marital': 3, 'records': 1, 'expenses': 48, 'assets': 2500, 'amount': 1000, 'price': 1685}
