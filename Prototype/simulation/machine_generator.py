from pulser.devices import Chadoq2
from dataclasses import replace
import yaml
import os

class MachineGenerator:

    @staticmethod
    def getMachine(name: str) -> Chadoq2:
        return replace(Chadoq2.to_virtual(), \
            **yaml.safe_load(open(
                os.path.join(
                    os.path.dirname(__file__),
                    "machines",
                    f"{name}.yml"
                )
            ))
        )
