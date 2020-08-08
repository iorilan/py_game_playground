"""
main.py
====================================
a sample module for doc test
"""
import datetime
def hello(name):
    """
    say hello to some nice name
    ----------
    string value of name
    """
    return f"[{datetime.datetime.now()}]: hello  {name}"


class Employee:
    """
        class to define a employee
        join date None means future date
    """

    def __init__(self, name, age=30, join_date=None):
        """
        something meaningful
        Parameters
        ---------
        name
            the name string 
        age
            age
        join_date
            date joined 
        """
        self.name = name
        self.age = age
        self.join_date = join_date

    def description(self):
        """
        return description of this person
        """
        return f"{self.name} [age: {self.age}] join date {self.join_date or 'is in future'}"