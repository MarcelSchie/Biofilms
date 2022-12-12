from dataclasses import dataclass, field
from typing import List, Tuple
from toolbox.utility import fluors_to_color

@dataclass
class Biofilm:
    name: str
    image_shape: Tuple[int]
    growth_duration: int
    sample: int
    voxel_sizes: list[float] = field(default_factory=list)
    fluors: list[str] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
    germs: list[str] = field(default_factory=list)
    thresholds: list[int] = field(default_factory=list)
    total_volumes: list[float] = field(default_factory=list)
    slice_volumes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        for xyz, voxel_size in zip(['x', 'y', 'z'], self.voxel_sizes):
            d['voxel_size ' + xyz] = voxel_size
        del d['voxel_sizes']
        for key, variable in zip(['fluors', 'germs', 'total_volumes', 'thresholds'], [self.fluors, self.germs, self.total_volumes, self.thresholds]):
            for i, entry in enumerate(variable):
                d[key[:-1] + str(i + 1)] = entry
            del d[key]
        return d

@dataclass
class Crosstalk:
    file: str
    germ: str
    fluors: List[str]
    main_channel: int
    main_fluor: str
    crosstalk: List[float]

    def to_dict(self) -> dict:
        d =  {'file': self.file, 'germ': self.germ, 'channel': self.main_channel, 'fluor': self.main_fluor}
        for fluor, crosstalk in zip(self.fluors, self.crosstalk):
            d[fluors_to_color[fluor]] = crosstalk
        return d

if __name__ == "__main__":
    pass