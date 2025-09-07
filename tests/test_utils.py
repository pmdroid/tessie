import pytest
from arcade_tdk.errors import ToolExecutionError

from tessie.utils import validate_vin


def test_validate_valid_vin():
    assert validate_vin("5YJ3E1EA4KF123456") is True


def test_validate_vin_empty():
    with pytest.raises(ToolExecutionError) as exc_info:
        validate_vin("")
    
    assert "VIN cannot be empty" in str(exc_info.value.message)


def test_validate_vin_too_short():
    with pytest.raises(ToolExecutionError) as exc_info:
        validate_vin("5YJ3E1EA4KF12345")
    
    assert "VIN must be exactly 17 characters" in str(exc_info.value.message)


def test_validate_vin_too_long():
    with pytest.raises(ToolExecutionError) as exc_info:
        validate_vin("5YJ3E1EA4KF1234567")
    
    assert "VIN must be exactly 17 characters" in str(exc_info.value.message)