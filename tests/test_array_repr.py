import numpy as np

from ch5mpy.array.repr import print_dataset


def test_repr_0D():
    assert print_dataset(np.array(1)) == "1\n"


def test_repr_1D():
    assert print_dataset(np.arange(10)) == "[0, 1, 2, ..., 7, 8, 9]\n"


def test_repr_2D():
    assert (
        print_dataset(np.arange(100).reshape((10, 10))) == "[[0, 1, 2, ..., 7, 8, 9],\n"
        " [10, 11, 12, ..., 17, 18, 19],\n"
        " [20, 21, 22, ..., 27, 28, 29],\n"
        " ...,\n"
        " [70, 71, 72, ..., 77, 78, 79],\n"
        " [80, 81, 82, ..., 87, 88, 89],\n"
        " [90, 91, 92, ..., 97, 98, 99]]\n"
    )


def test_repr_3D():
    assert (
        print_dataset(np.arange(40).reshape((10, 2, 2))) == "[[[0, 1],\n"
        "  [2, 3]],\n"
        "\n"
        " [[4, 5],\n"
        "  [6, 7]],\n"
        "\n"
        " [[8, 9],\n"
        "  [10, 11]],\n"
        "\n"
        " ...,\n"
        "\n"
        " [[28, 29],\n"
        "  [30, 31]],\n"
        "\n"
        " [[32, 33],\n"
        "  [34, 35]],\n"
        "\n"
        " [[36, 37],\n"
        "  [38, 39]]]\n"
    )


def test_repr_4D():
    assert (
        print_dataset(np.arange(80).reshape((10, 2, 2, 2))) == "[[[[0, 1],\n"
        "   [2, 3]],\n"
        "\n"
        "  [[4, 5],\n"
        "   [6, 7]]],\n"
        "\n"
        "\n"
        " [[[8, 9],\n"
        "   [10, 11]],\n"
        "\n"
        "  [[12, 13],\n"
        "   [14, 15]]],\n"
        "\n"
        "\n"
        " [[[16, 17],\n"
        "   [18, 19]],\n"
        "\n"
        "  [[20, 21],\n"
        "   [22, 23]]],\n"
        "\n"
        "\n"
        " ...,\n"
        "\n"
        "\n"
        " [[[56, 57],\n"
        "   [58, 59]],\n"
        "\n"
        "  [[60, 61],\n"
        "   [62, 63]]],\n"
        "\n"
        "\n"
        " [[[64, 65],\n"
        "   [66, 67]],\n"
        "\n"
        "  [[68, 69],\n"
        "   [70, 71]]],\n"
        "\n"
        "\n"
        " [[[72, 73],\n"
        "   [74, 75]],\n"
        "\n"
        "  [[76, 77],\n"
        "   [78, 79]]]]\n"
    )
