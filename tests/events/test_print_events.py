import os

import numpy as np
from pytest import approx

from pymt.events.manager import EventManager
from pymt.events.printer import PrintEvent


def test_one_event(tmpdir, with_earth_and_air):
    with tmpdir.as_cwd():
        foo = PrintEvent(port="air_port", name="air__density", format="vtk")

        with EventManager(((foo, 1.),)) as mngr:
            assert mngr.time == approx(0.)

            mngr.run(1.)
            assert mngr.time == approx(1.)

            mngr.run(1.)
            assert mngr.time == approx(1.)

            for time in np.arange(1., 2., .1):
                mngr.run(time)
                assert mngr.time == approx(time)

            mngr.run(2.)
            assert mngr.time == approx(2.)

            for time in np.arange(2., 5., .1):
                mngr.run(time)
                assert mngr.time == approx(time)

        assert os.path.isfile("air__density_0000.vtu")
        assert os.path.isfile("air__density_0001.vtu")
        assert os.path.isfile("air__density_0002.vtu")
        assert os.path.isfile("air__density_0003.vtu")


def test_two_events(tmpdir, with_earth_and_air):
    with tmpdir.as_cwd():
        foo = PrintEvent(port="air_port", name="air__density", format="vtk")
        bar = PrintEvent(port="air_port", name="air__temperature", format="vtk")

        with EventManager(((foo, 1.), (bar, 1.2))) as mngr:
            mngr.run(1.)
            assert os.path.isfile("air__density_0000.vtu")
            os.remove("air__density_0000.vtu")

            mngr.run(2.)
            assert os.path.isfile("air__density_0001.vtu")
            assert os.path.isfile("air__temperature_0000.vtu")
            assert mngr.time == approx(2.)

            mngr.run(5.)
            assert mngr.time == approx(5.)

        assert os.path.isfile("air__density_0002.vtu")
        assert os.path.isfile("air__density_0003.vtu")
        assert os.path.isfile("air__density_0004.vtu")
        assert not os.path.exists("air__density_0005.vtu")

        assert os.path.isfile("air__temperature_0001.vtu")
        assert os.path.isfile("air__temperature_0002.vtu")
        assert os.path.isfile("air__temperature_0003.vtu")
        assert not os.path.exists("air__temperature_0004.vtu")