#!/usr/bin/python3
'''
    Define the class City.
'''
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    '''
        Define the class City that inherits from BaseModel.
    '''
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="delete")
    else:
        name = ""
        state_id = ""

        @property
        def places(self):
            '''
                Getter for places when using FileStorage system
                Returns:
                    A list of Place objects associated with the current City
            '''
            cls_dict = models.storage.all(models.classes["Place"])
            places_in_city = []
            current_city = self.id
            for key, value in cls_dict.items():
                if value.city_id == current_city:
                    places_in_city.append(value)
            return places_in_city
