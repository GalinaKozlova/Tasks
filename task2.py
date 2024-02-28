print ("Hello world!")
from __future__ import annotations
from collections.abc import Iterator
import datetime
from typing import Optional, Union, Iterable

class Client:
    def _init_(
        self,
        Status: int,
        Seniority: int,
        Home: int,
        Time: int,
        Age: int,
        Marital: int,
        Job: int,
        Expenses: float,
        Income: int,
        Assets: float,
        Debt: float,
        Amount: float,
        Price: float,
        client_type: Optional[str] = None,
    ) -> None:
        self.status=Status
        self.senority=Seniority
        self.home=Home
        self.time=Time
        self.age=Age
        self.marital=Marital
        self.job=Job
        self.expenses=Expenses
        self.income=Income
        self.assets=Assets
        self.debt=Debt
        self.amount=Amount
        self.price=Price
        self.client_type=client_type
        self.classification: Optional[str] = None

def __repr__(self) -> str:
        if self.client_type is None:
            known_unknown = "UnknownSample"
        else:
            known_unknown = "KnownSample"
        if self.classification is None:
            classification = ""
        else:
            classification = f", classification={self.classification!r}"
        return (
            f"{known_unknown}("
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
            f"{classification}"
            f")"
        )

def classify(self, classification: str) -> None:
        self.classification = classification

def matches(self) -> bool:
        return self.client_type == self.classification
   