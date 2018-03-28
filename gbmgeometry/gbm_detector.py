__author__ = "drjfunk"
import numpy as np
from astropy.coordinates import SkyCoord, get_sun, get_body
from spherical_geometry.polygon import SphericalPolygon
import astropy.units as u

from .gbm_frame import GBMFrame


class GBMDetector(object):
    def __init__(self, name, quaternion, sc_pos=None, time=None):
        """
        
        :param name: 
        :param quaternion: 
        :param sc_pos: 
        :param time: 
        """

        self._name = name

        self.update_position(quaternion, sc_pos, time)

        self._xyz = np.array([np.cos(self._az)*np.sin(self._zen), np.sin(self._az)*np.sin(self._zen), np.cos(self._zen)])

        


    def update_position(self, quaternion, sc_pos=None, time=None):
        """
        
        :param quaternion: 
        :param sc_pos: 
        :param time: 
        :return: 
        """

        self._time = time

        q1, q2, q3, q4 = quaternion

        if sc_pos is not None:
            scx, scy, scz = sc_pos

        else:
            scx = None
            scy = None
            scz = None

        self._center = SkyCoord(self._az * u.deg,
                                self._zen * u.deg,
                                unit='deg',
                                frame=GBMFrame(quaternion_1=q1,
                                               quaternion_2=q2,
                                               quaternion_3=q3,
                                               quaternion_4=q4,
                                               sc_pos_X=scx,
                                               sc_pos_Y=scy,
                                               sc_pos_Z=scz,
                                               ))

        if self._time is not None:
            # we can calculate the sun position
            tmp_sun = get_sun(self._time).icrs

                        
            self._sun_position = SkyCoord(tmp_sun.ra.deg,tmp_sun.dec.deg,unit='deg', frame='icrs').transform_to(self._center.frame)

            tmp_earth = get_body('earth',time=self._time).icrs
            
            self._earth_position = SkyCoord(tmp_earth.ra.deg, tmp_earth.dec.deg, unit='deg', frame='icrs').transform_to(self._center.frame)

        self._quaternion = quaternion
        self._sc_pos = sc_pos


    def set_quaternion(self, quaternion):
        """
        Parameters
        ----------
        quaternion

        """

        self._quaternion = quaternion

        q1, q2, q3, q4 = quaternion

        if self._sc_pos is not None:
            scx, scy, scz = self._sc_pos

        else:
            scx = None
            scy = None
            scz = None

        self._center = SkyCoord(self._az* u.deg,
                                self._zen * u.deg,
                                unit='deg',
                                frame=GBMFrame(quaternion_1=q1,
                                               quaternion_2=q2,
                                               quaternion_3=q3,
                                               quaternion_4=q4,
                                               sc_pos_X=scx,
                                               sc_pos_Y=scy,
                                               sc_pos_Z=scz,
                                               ))

    def set_sc_pos(self, sc_pos):
        """
        Parameters
        ----------
        quaternion

        """

        q1, q2, q3, q4 = self._quaternion

        if sc_pos is not None:
            scx, scy, scz = sc_pos

        else:
            scx = None
            scy = None
            scz = None

        self._center = SkyCoord(self._az * u.deg,
                                self._zen * u.deg,
                                unit='deg',
                                frame=GBMFrame(quaternion_1=q1,
                                               quaternion_2=q2,
                                               quaternion_3=q3,
                                               quaternion_4=q4,
                                               sc_pos_X=scx,
                                               sc_pos_Y=scy,
                                               sc_pos_Z=scz,
                                               ))

    def get_fov(self, radius, fermi_frame=False):
        """
        Returns
        -------
        array of RA and DEC

        """

        steps = 500

        if fermi_frame:
            fermi = self._center

            poly = SphericalPolygon.from_cone(fermi.lon.value,
                                              fermi.lat.value,
                                              radius,
                                              steps=steps)


        else:

            j2000 = self._center.icrs

            poly = SphericalPolygon.from_cone(j2000.ra.value,
                                              j2000.dec.value,
                                              radius,
                                              steps=steps)

        # ra, dec
        return [p for p in poly.to_radec()][0]

    def get_center(self):
        return self._center


    @property
    def sun_position(self):

        return self._sun_position

    @property
    def sun_angle(self):

        return self._center.separation(self._sun_position)

    @property
    def earth_position(self):

        return self._earth_position

    @property
    def earth_angle(self):

        return self._center.separation(self._earth_position)


    @property
    def center(self):

        return self._center

    @property
    def name(self):

        return self._name

    @property
    def az(self):

        return self._az

    @property
    def zen(self):

        return self._zen

    @property
    def xyz(self):

        return self._xyz

    

    
    @property
    def mount_point(self):

        return self._mount_point


class NaI0(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 45.89
        self._zen = 90 - 20.58

        self._mount_point = np.array([96.1, 80.4, 107.6])

        super(NaI0, self).__init__('n0', quaternion, sc_pos, time)


class NaI1(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 45.11
        self._zen = 90 - 45.31
        self._mount_point = np.array([101.1, 72.8, 72.1])

        super(NaI1, self).__init__('n1', quaternion, sc_pos, time)


class NaI2(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 58.44
        self._zen = 90 - 90.21
        self._mount_point = np.array([109.0, 58.1, 99.0])

        super(NaI2, self).__init__('n2', quaternion, sc_pos, time)


class NaI3(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 314.87
        self._zen = 90 - 45.24
        self._mount_point = np.array([97.7, -76.3, 102.5])

        super(NaI3, self).__init__('n3', quaternion, sc_pos, time)


class NaI4(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 303.15
        self._zen = 90. - 90.27
        self._mount_point = np.array([109.0, -57.5, 83.6])

        super(NaI4, self).__init__('n4', quaternion, sc_pos, time)


class NaI5(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 3.35
        self._zen = 90 - 89.97
        self._mount_point = np.array([99.6, -49.7, 100.1])

        super(NaI5, self).__init__('n5', quaternion, sc_pos, time)


class NaI6(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 224.93
        self._zen = 90 - 20.43
        self._mount_point = np.array([-95.8, -80.3, 107.1])

        super(NaI6, self).__init__('n6', quaternion, sc_pos, time)


class NaI7(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 224.62
        self._zen = 90 - 46.18
        self._mount_point = np.array([-100.6, -72.5, 71.6])

        super(NaI7, self).__init__('n7', quaternion, sc_pos, time)


class NaI8(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 236.61
        self._zen = 90 - 89.97
        self._mount_point = np.array([-108.4, -57.2, 99.0])

        super(NaI8, self).__init__('n8', quaternion, sc_pos, time)


class NaI9(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 135.19
        self._zen = 90 - 45.55
        self._mount_point = np.array([-97.5, 76.5, 102.5])

        super(NaI9, self).__init__('n9', quaternion, sc_pos, time)


class NaIA(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """

        self._az = 123.73
        self._zen = 90 - 90.42
        self._mount_point = np.array([-108.7, 57.7, 83.7])

        super(NaIA, self).__init__('na', quaternion, sc_pos, time)


class NaIB(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 183.74
        self._zen = 90 - 90.32
        self._mount_point = np.array([-99.3, 50.0, 100.2])

        super(NaIB, self).__init__('nb', quaternion, sc_pos, time)


class BGO0(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 0.
        self._zen = 0.
        self._mount_point = np.array([126.05, 0.13, 63.32])

        super(BGO0, self).__init__('b0', quaternion, sc_pos, time)


class BGO1(GBMDetector):
    def __init__(self, quaternion, sc_pos=None, time=None):
        """

        Parameters
        ----------
        quaternion
        """
        self._az = 180.
        self._zen = 0.
        self._mount_point = np.array([-126.14, 0.01, 67.22])

        super(BGO1, self).__init__('b1', quaternion, sc_pos, time)
