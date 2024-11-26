import os
import sqlite3
from abc import ABC


class Model(ABC):
    def __init__(self)-> None:
        self.database = sqlite3.connect("./app/models/jobs.db")
        self.cursor = self.database.cursor()
