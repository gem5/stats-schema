
from typing import Any, Dict, KeysView, List, Optional, Tuple, Union

from .statistic import Statistic
from .util import TimeConversion


class Model:

    type: Optional[str]
    timeConversion: Optional[TimeConversion]

    def __init__(self, type: Optional[str] = None,
                 timeConversion: Optional[TimeConversion] = None,
                 **kwargs: Dict[str, Union["Model",Statistic,List["Model"]]]):
        self.type = type
        self.timeConversion = timeConversion

        for key,value in kwargs:
            setattr(self, key, value)

    def __init__(self, data: Dict[str, Any]):
        for prop in ('type', 'timeConversion'):
            if prop in data:
                setattr(self, prop, data.pop(prop))
            else:
                setattr(self, prop, None)

        for prop,value in data.items():
            if type(value) is list:
                setattr(self, prop, [Model.load(model) for model in value])
            else:
                try:
                    setattr(self, prop, Statistic.load(value))
                except KeyError:
                    # If we can't load it as a statistic then it must be a model
                    # Note that currently models can have *anything*, so this
                    # doesn't do any checking, it should always succeed
                    setattr(self, prop, Model.load(value))

    @classmethod
    def load(cls, data: Dict[str, Union["Model",Statistic,List["Model"]]]) -> "Model":
        return cls(data)
