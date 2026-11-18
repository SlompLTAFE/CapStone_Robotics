import pytest
from xarm_toolkit.targets.ari_tracker import ARIPersonTracker
from xarm_toolkit.targets.target_source import TargetSelectionCancelled


def test_tracker_uses_default_topic():
    tracker = ARIPersonTracker()

    assert tracker._topic == "/UNRESOLVED_ari_person_topic"


def test_tracker_uses_custom_topic():
    tracker = ARIPersonTracker("/test/person_topic")

    assert tracker._topic == "/test/person_topic"


def test_get_target_raises_when_no_target_exists():
    tracker = ARIPersonTracker()

    with pytest.raises(TargetSelectionCancelled):
        tracker.get_target()


def test_message_conversion_is_not_implemented_yet():
    tracker = ARIPersonTracker()

    with pytest.raises(NotImplementedError):
        tracker._to_target(object())


def test_message_callback_does_not_store_unconverted_message():
    tracker = ARIPersonTracker()

    with pytest.raises(NotImplementedError):
        tracker._on_msg(object())

    assert tracker._latest is None
