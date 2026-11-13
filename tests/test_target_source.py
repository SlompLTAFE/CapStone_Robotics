
import pytest

from xarm_toolkit import TargetSource
from xarm_toolkit import MockClickTarget


def test_mock_is_target_source():
    assert issubclass(MockClickTarget, TargetSource)


def test_target_source_cannot_be_instantiated():
    with pytest.raises(TypeError):
        TargetSource()

