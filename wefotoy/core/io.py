import h5py
import torch
from typing import Literal


def _open(file: str, mode: Literal['r', 'w', 'a'] = 'a') -> h5py.File:
    return h5py.File(name=f'{file}.h5', mode=mode)


def _require_group_recursive(file: h5py.File, *group: str) -> h5py.Group:
    _grp = file
    for grp in group:
        _grp = _grp.require_group(grp)  # type: ignore
    return _grp


def write_tensor(path: str, tag: str, data: torch.Tensor) -> None:
    with _open(path) as h5file:
        _tag = tag.split('/')
        _grp = _require_group_recursive(h5file, *_tag[:-1])
        try:
            _dset = _grp.create_dataset(_tag[-1], data=data.cpu().numpy())  # type: ignore
        except ValueError:
            del _grp[_tag[-1]]
            _dset = _grp.create_dataset(_tag[-1], data=data.cpu().numpy())  # type: ignore
