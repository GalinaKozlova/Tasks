from __future__ import annotations
import collections
import datetime
from math import isclose
from typing import (
    cast,
    Optional,
    Union,
    Iterator,
    Iterable,
    Counter,
    Callable,
    Protocol,
)
import weakref


class Client:
    def __init__(
        self,
        status: int,
        seniority: int,
        home: int,
        time: int,
        age: int,
        marital: int,
        job: int,
        expenses: float,
        income: int,
        assets: float,
        debt: float,
        amount: float,
        price: float,
        client_type: Optional[str] = None,
    ) -> None:
        self.status = status
        self.senority = seniority
        self.home = home
        self.time = time
        self.age = age
        self.marital = marital
        self.job = job
        self.expenses = expenses
        self.income = income
        self.assets = assets
        self.debt = debt
        self.amount = amount
        self.price = price
        self.client_type = client_type
        self.classification: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"status={self.status}, "
            f"seniotity={self.seniority}, "
            f"home={self.home}, "
            f"time={self.time}, "
            f"age={self.age}, "
            f"marital={self.marital}, "
            f"job={self.job}, "
            f"expenses={self.expenses}, "
            f"income={self.income}, "
            f"debt={self.debt}, "
            f"amount={self.amount}, "
            f"price={self.price}, "
            f"client_type={self.client_type!r}"
            f")"
        )


class KnownClient(Client):
    def __init__(
        self,
        status: int,
        seniority: int,
        home: int,
        time: int,
        age: int,
        marital: int,
        job: int,
        expenses: float,
        income: int,
        assets: float,
        debt: float,
        amount: float,
        price: float,
    ) -> None:
        super().__init__(
            status=status,
            senority=seniority,
            home=home,
            time=time,
            age=age,
            marital=marital,
            job=job,
            expenses=expenses,
            income=income,
            assets=assets,
            debt=debt,
            amount=amount,
            price=price,
        )
        self.client_type = client_type

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"status={self.status}, "
            f"seniotity={self.seniority}, "
            f"home={self.home}, "
            f"time={self.time}, "
            f"age={self.age}, "
            f"marital={self.marital}, "
            f"job={self.job}, "
            f"expenses={self.expenses}, "
            f"income={self.income}, "
            f"debt={self.debt}, "
            f"amount={self.amount}, "
            f"price={self.price}, "
            f"client_type={self.client_type!r}"
            f")"
        )
    
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "KnownClient":
        if row["client_type"] not in {"Can pay", "Can't pay"}:
            raise InvalidClientError(f"invalid client in {row!r}")
        try:
            return cls(
                client_type=row["client_type"],
                status=int(row["status"]),
                seniority=int(row["seniority"]),
                home=int(row["home"]),
                time=int(row["time"]),
                age=int(row["age"]),
                marital=int(row["marital"]),
                job=int(row["job"]),
                expenses=float(row["expenses"]),
                income=int(row["income"]),
                assets=float(row["assets"]),
                debt=float(row["debt"]),
                amount=float(row["amount"]),
                price=float(row["price"]),
            )
        except ValueError as ex:
            raise InvalidClientError(f"invalid {row!r}")
        

class TrainingKnownClient(KnownClient):
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> TrainingKnownClient:
        return cast(TrainingKnownClient, super().from_dict(row))
    

class TestingKnownClient(KnownClient):
    def __init__(
            self,
            /,
            status: int,
            seniority: int,
            home: int,
            time: int,
            age: int,
            marital: int,
            job: int,
            expenses: float,
            income: int,
            assets: float,
            debt: float,
            amount: float,
            price: float
    ) -> None:
        super().__init__(
            client_type=client_type,
            status=status,
            senority=seniority,
            home=home,
            time=time,
            age=age,
            marital=marital,
            job=job,
            expenses=expenses,
            income=income,
            assets=assets,
            debt=debt,
            amount=amount,
            price=price,
        )
        self.classification = client_type

    def matches(self) -> bool:
        return self.client_type == self.classification
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"status={self.status}, "
            f"seniotity={self.seniority}, "
            f"home={self.home}, "
            f"time={self.time}, "
            f"age={self.age}, "
            f"marital={self.marital}, "
            f"job={self.job}, "
            f"expenses={self.expenses}, "
            f"income={self.income}, "
            f"debt={self.debt}, "
            f"amount={self.amount}, "
            f"price={self.price}, "
            f"client_type={self.client_type!r}"
            f")"
        )
    
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "TestingKnownClient":
        return cast(TestingKnownClient, super().from_dict(row))
    

class UnknownClient(Client):
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "UnknownClient":
        if set(row.keys()) != {
            "status",
            "seniority",
            "home",
            "time",
            "age",
            "marital",
            "job",
            "expenses",
            "income",
            "assets",
            "debt",
            "amount",
            "price",
        }:
            raise InvalidClientError(f"invalid clients in {row!r}")
        try:
            return cls(
                client_type=row["client_type"],
                status=int(row["status"]),
                seniority=int(row["seniority"]),
                home=int(row["home"]),
                time=int(row["time"]),
                age=int(row["age"]),
                marital=int(row["marital"]),
                job=int(row["job"]),
                expenses=float(row["expenses"]),
                income=int(row["income"]),
                assets=float(row["assets"]),
                debt=float(row["debt"]),
                amount=float(row["amount"]),
                price=float(row["price"]),
            )
        except(ValueError, KeyError) as ex:
            raise InvalidClientError (f"invalid {row!r}")


class ClassifiedClient (Client):
    def __init__(self, client_type: str, client: UnknownClient) -> None:
        super().__init__(
            client_type=client.client_type,
            status=client.status,
            senority=client.seniority,
            home=client.home,
            time=client.time,
            age=client.age,
            marital=client.marital,
            job=client.job,
            expenses=client.expenses,
            income=client.income,
            assets=client.assets,
            debt=client.debt,
            amount=client.amount,
            price=client.price,
        )
        self.classification = client_type

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"status={self.status}, "
            f"seniotity={self.seniority}, "
            f"home={self.home}, "
            f"time={self.time}, "
            f"age={self.age}, "
            f"marital={self.marital}, "
            f"job={self.job}, "
            f"expenses={self.expenses}, "
            f"income={self.income}, "
            f"debt={self.debt}, "
            f"amount={self.amount}, "
            f"price={self.price}, "
            f"client_type={self.client_type!r}"
            f")"
        )
    

class Hyperparameter:
    def __init__(self, training: "TrainingData") -> None:
        self.data: weakref.ReferenceType["TrainingData"] = weakref.ref(training)
        self.quality: float = 0.0
        
    def test(self) -> None:
        training_data: Optional["TrainingData"] = self.data()
        if not training_data:
            raise RuntimeError("Broken Weak Reference")
        pass_count, fail_count = 0, 0
        for client in training_data.testing:
            client.classification = self.classify(client)
            if client.matches():
                pass_count += 1
            else:
                fail_count += 1
        self.quality = pass_count / (pass_count + fail_count)


class TrainingData:
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: datetime.datetime
        self.tested: datetime.datetime
        self.training: list[TrainingKnownClient] = []
        self.testing: list[TestingKnownClient] = []
        self.tuning: list[Hyperparameter] = []

    def load(self, raw_data_iter: Iterable[dict[str, str]]) -> None:
        for n, row in enumerate(raw_data_iter):
            try:
                if n % 5 == 0:
                    test = TestingKnownClient.from_dict(row)
                    self.testing.append(test)
                else:
                    train = TrainingKnownClient.from_dict(row)
                    self.training.append(train)
            except InvalidClientError as ex:
                print(f"Row {n+1}: {ex}")
                return
        self.uploaded = datetime.datetime.now(tz=datetime.timezone.utc)

    def test(self, parameter: Hyperparameter) -> None:
        parameter.test()
        self.tuning.append(parameter)
        self.tested = datetime.datetime.now(tz=datetime.timezone.utc)

    def classify(
        self, parameter: Hyperparameter, sample: UnknownClient
    ) -> ClassifiedClient:
        return ClassifiedClient(
            classification=parameter.classify(sample), sample=sample
        )