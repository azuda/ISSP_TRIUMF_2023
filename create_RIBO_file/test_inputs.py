from inputs import get_foil_options, get_anything_else, validate
import pytest
from unittest.mock import patch


@pytest.fixture
def foil():
    test_args = ["py .\\Create_ribo_file\\inputs.py", "--quantity", "10", "--shape", "d", "--length", "0.9144",
                 "--height", "0.1524", "--thickness", "0.00254", "--rotation", "0", "--squish", "1", "--filename", "test_ribo_file"]
    with patch("sys.argv", test_args):
        return get_foil_options()


@pytest.fixture
def pizza_foil():
    test_args = ["py .\\Create_ribo_file\\inputs.py", "--quantity", "10", "--shape", "symm", "--length", "0.9144",
                 "--height", "0.1524", "--thickness", "0.00254", "--rotation", "0", "--squish", "1", "--filename", "test_ribo_file"]
    with patch("sys.argv", test_args):
        return get_anything_else()


@pytest.fixture
def horseshoe_foil():
    test_args = ["py .\\Create_ribo_file\\inputs.py", "--quantity", "10", "--shape", "ring", "--length", "0.9144",
                 "--height", "0.1524", "--thickness", "0.00254", "--rotation", "0", "--squish", "1", "--filename", "test_ribo_file"]
    with patch("sys.argv", test_args):
        return get_anything_else()


@pytest.fixture
def invalid_shape():
    test_args = ["py .\\Create_ribo_file\\inputs.py", "--quantity", "10", "--shape", "invalid", "--length", "0.9144",
                 "--height", "0.1524", "--thickness", "0.00254", "--rotation", "0", "--squish", "1", "--filename", "test_ribo_file"]
    with patch("sys.argv", test_args):
        return validate()


@pytest.fixture
def invalid_filename():
    test_args = ["py .\\Create_ribo_file\\inputs.py", "--quantity", "10", "--shape", "d", "--length", "0.9144",
                 "--height", "0.1524", "--thickness", "0.00254", "--rotation", "0", "--squish", "1", "--filename", "test_ribo_file_long_filename"]
    with patch("sys.argv", test_args):
        return validate()


def test_get_foil_options(foil):
    assert foil["quantity"] == 10
    assert foil["shape"] == "d"
    assert foil["length"] == 0.9144
    assert foil["height"] == 0.1524
    assert foil["thickness"] == 0.00254
    assert foil["rotation"] == 0
    assert foil["squish"] == 1
    assert foil["filename"] == "test_ribo_file"


def test_get_anything_else_pizza(pizza_foil):
    assert pizza_foil["r1"] == 0.9144
    assert pizza_foil["th"] == 0.7853981633974483
    assert pizza_foil["m"] == 1


def test_get_anything_else_horseshoe(horseshoe_foil):
    assert horseshoe_foil["r1"] == 0.9144
    assert horseshoe_foil["r2"] == 0.3644
    assert horseshoe_foil["th"] == 0.7853981633974483
    assert horseshoe_foil["m"] == 1


def test_invalid_shape(invalid_shape):
    with pytest.raises(ValueError, match="Invalid foil shape"):
        invalid_shape()


def test_invalid_filename(invalid_filename):
    with pytest.raises(ValueError, match="File name must be less than 20 characters"):
        invalid_filename()
