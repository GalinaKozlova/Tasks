from __future__ import annotations

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score
from pathlib import Path

import datetime
import csv
import weakref

from typing import (
    cast,
    Optional,
    Union,
    Iterable
)


class InvalidClientError(ValueError):
    """Файл-исходник имеет недопустимое представление данных"""


class Client:
    def __init__(
            self,
            seniority: int,
            home: int,
            age: int,
            marital: int,
            records: int,
            expenses: int,
            assets: int,
            amount: int,
            price: int
    ) -> None:
        self.seniority = seniority
        self.home = home
        self.age = age
        self.marital = marital
        self.records = records
        self.expenses = expenses
        self.assets = assets
        self.amount = amount
        self.price = price

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"seniority={self.seniority},"
            f"home={self.home},"
            f"age={self.age},"
            f"marital={self.marital},"
            f"records={self.records},"
            f"expenses={self.assets},"
            f"amount={self.amount},"
            f"price={self.price}"
            f")"
        )
    

class KnownClient(Client):
    def __init__(
        self,
        status: int,
        seniority: int,
        home: int,
        age: int,
        marital: int,
        records: int,
        expenses: int,
        assets: int,
        amount: int,
        price: int
    ) -> None:
        super().__init__(
            seniority=seniority,
            home=home,
            age=age,
            marital=marital,
            records=records,
            expenses=expenses,
            assets=assets,
            amount=amount,
            price=price
        )
        self.status = status

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"seniority={self.seniority},"
            f"home={self.home},"
            f"age={self.age},"
            f"marital={self.marital},"
            f"records={self.records},"
            f"expenses={self.assets},"
            f"amount={self.amount},"
            f"price={self.price},"
            f"status={self.status!r}"
            f")"
        )
    
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "KnownClient":
        if row["status"] not in {"0", "1", "-1"}:  # 0 - дать, 1 - не дать, -1 - ошибка
            raise InvalidClientError(f"invalid status in {row!r}")
        try:
            return cls(
                status=int(row["status"]),
                seniority=int(row["seniority"]),
                home=int(row["home"]),
                age=int(row["age"]),
                marital=int(row["marital"]),
                records=int(row["records"]),
                expenses=int(row["expenses"]),
                amount=int(row["amount"]),
                price=int(row["price"]),
            )
        except ValueError as ex:
            raise InvalidClientError(f"invalid {row!r}")
        

class TrainingKnownClient(KnownClient):
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "TrainingKnownClient":
        return cast(TrainingKnownClient, super().from_dict(row))
    

class TestingKnownClient(KnownClient):
    def __init__(
        self,
        status: int,
        seniority: int,
        home: int,
        age: int,
        marital: int,
        records: int,
        expenses: int,
        assets: int,
        amount: int,
        price: int,
        classification: Optional[int] = None
    ) -> None:
        super().__init__(
            status,
            seniority,
            home,
            age,
            marital,
            records,
            expenses,
            assets,
            amount,
            price
        )
        self.classification = classification

    def matches(self) -> bool:
        self.status = self.classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"seniority={self.seniority},"
            f"home={self.home},"
            f"age={self.age},"
            f"marital={self.marital},"
            f"records={self.records},"
            f"expenses={self.assets},"
            f"amount={self.amount},"
            f"price={self.price},"
            f"status={self.status!r}"
            f"classification={self.classification!r}"
            f")"
        )
    

class UnknownClient(Client):
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "UnknownClient":
        if set(row.keys()) != {
            "seniority",
            "home",
            "age",
            "marital",
            "records",
            "assets",
            "amount",
            "price",
        }:
            raise InvalidClientError(f"invalid fields in {row!r}")
        try:
            return cls(
                status=int(row["status"]),
                seniority=int(row["seniority"]),
                home=int(row["home"]),
                age=int(row["age"]),
                marital=int(row["marital"]),
                records=int(row["records"]),
                expenses=int(row["expenses"]),
                amount=int(row["amount"]),
                price=int(row["price"]),
            )
        except ValueError:
            raise InvalidClientError(f"invalid status in {row!r}")
        

class ClassifiedClient(Client):
    def __init__(self, classification: int, client: UnknownClient) -> None:
        super().__init__(
            seniority=client.seniority,
            home=client.home,
            age=client.age,
            marital=client.marital,
            records=client.records,
            expenses=client.expenses,
            assets=client.assets,
            amount=client.amount,
            price=client.price,
        )
        self.classification = classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"seniority={self.seniority},"
            f"home={self.home},"
            f"age={self.age},"
            f"marital={self.marital},"
            f"records={self.records},"
            f"expenses={self.assets},"
            f"amount={self.amount},"
            f"price={self.price},"
            f"classification={self.classification!r}"
            f")"
        )
   

class Hyperparameter:
    def __init__(self, max_depth: int, min_samples_split: int, training: "TrainingData") -> None:
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.data: weakref.ReferenceType["TrainingData"] = weakref.ref(training)
        self.quality: float

    def test(self) -> None:
        trainingData: Optional["TrainingData"] = self.data()
        if not trainingData:
            raise RuntimeError("Broken Waek Reference")
        test_data = trainingData.testing
        x_test = TrainingData.get_list_clients(test_data)
        y_test = TrainingData.get_statuses_clients(test_data)
        y_predict = self.classify_list(x_test)
        self.quality = roc_auc_score(y_test, y_predict)
        for i in range(len(y_predict)):
            test_data[i].classification = y_predict[i]

    def classify_list(self, clients: list[Union[UnknownClient, TestingKnownClient]]) -> list:
        training_data = self.data
        if not training_data:
            raise RuntimeError("No training object")
        x_predict = TrainingData.get_list_clients(clients)
        x_train = TrainingData.get_list_clients(training_data)
        y_train = TrainingData.get_statuses_clients(training_data)

        classifier = DecisionTreeClassifier(max_depth=self.max_depth, min_samples_split=self.min_samples_split)
        classifier = classifier.fit(x_train, y_train)
        return classifier.predict(x_predict).tolist()
    

class TrainingData:
    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: datetime.datetime
        self.tested: datetime.datetime
        self.training: list[TrainingKnownClient] = []
        self.testing: list[TestingKnownClient] = []
        self.tuning: list[Hyperparameter] = []

    def load(self, Client: Iterable(dict[str, str])) -> None:
        for n, row in enumerate(Client):
            try:
                if n % 5 == 0:
                    test = TestingKnownClient.from_dict(row)
                    self.testing.append(test)
                else:
                    train = TrainingKnownClient.from_dict(row)
                    self.training.append(train)
            except InvalidClientError as ex:
                print(f"row {n + 1}: {ex}")
                return
        self. uploaded = datetime.datetime.now(tz=datetime.timezone.utc)

    def test(self, parameter: Hyperparameter) -> None:
        parameter.test()
        self.tuning.append(parameter)
        self.tested = datetime.datetime.now(tz=datetime.timezone.utc)

    def classify(self, parameter: Hyperparameter, client: Client) -> Client:
        classification = parameter.classify(client)
        client.classify(classification)
        return client
    
    @staticmethod
    def get_list_clients(clients: list[Client]) -> list:
        return [
            [
                client.seniority,
                client.home,
                client.age,
                client.marital,
                client.records,
                client.expenses,
                client.assets,
                client.amount,
                client.price
            ]
            for client in clients
        ]
    @staticmethod
    def get_statuses_clients(clients: list[KnownClient]) -> list:
        return [client.status for client in clients]
    
    @staticmethod
    def get_client_as_list(client: Client) -> list:
        return [
            [
                client.seniority,
                client.home,
                client.age,
                client.marital,
                client.records,
                client.expenses,
                client.assets,
                client.amount,
                client.price
            ]
        ]
    

class ClientReader:
    target_class = Client
    header = [
        "seniority",
        "home",
        "age",
        "marital",
        "records",
        "expenses",
        "assets",
        "amount",
        "price",
        "status",
    ]

    def __init__(self, source: Path) -> None:
        self.source = source

    def client_iter(self) -> Iterator[Client]:
        target_class = self.target_class
        with self.source.open() as source_file:
            reader = csv.DictReader(source_file, self.header)
            for row in reader:
                try:
                    client = target_class(
                        seniority=int(row["seniority"]),
                        home=int(row["home"]),
                        age=int(row["age"]),
                        marital=int(row["marital"]),
                        records=int(row["records"]),
                        expenses=int(row["expenses"]),
                        assets=int(row["assets"]),
                        amount=int(row["amount"]),
                        price=int(row["price"]),
                    )
                except ValueError as exception:
                    raise BadClientRow(f"invalid {row!r}")
                yield client


class BadClientRow(ValueError):
    pass
