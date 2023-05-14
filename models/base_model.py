#!/usr/bin/python3
"""BaseModel class"""
import models
import uuid
from datetime import datetime


class BaseModel:
    """Creates a new BaseModel object"""

    def __init__(self, *args, **kwargs):
        """Initializes a new BaseModel object"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """Updates the public instance attribute updated_at"""
        self.updated_at = datetime.today()

    def to_dict(self):
        """Returns a dictionary of __dict__ of the instance"""
        my_dict = self.__dict__.copy()
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict["__class__"] = self.__class__.__name__
        return my_dict

    def __str__(self):
        """Print a string representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
