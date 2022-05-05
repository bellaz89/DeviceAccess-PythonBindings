import _da_python_bindings as pb
import numpy as np
import enum


def setDMapFilePath(dmapFilePath):
    # dmapFilePath	Relative or absolute path of the dmap file (directory and file name).
    pb.setDmapFile(dmapFilePath)


def getDMapFilePath(dmapFilePath):
    return pb.getDmapFile()


class Device:
    def __init__(self, aliasName=None):
        self.aliasName = aliasName
        if aliasName:
            self._device = pb.getDevice(aliasName)
        else:
            self._device = pb.getDevice_no_alias()

    def open(self, aliasName=None):
        if not aliasName:
            if self.aliasName:
                self._device.open()
            else:
                raise SyntaxError(
                    "No backend is assigned: the device is not opened"
                )
        elif not self.aliasName:
            self.aliasName = aliasName
            self._device.open(aliasName)
        else:
            raise SyntaxError(
                "Device has not been opened correctly: the device is not opened"
            )

    def close(self):
        self._device.close()

    def getTwoDRegisterAccessor(self, userType, registerPathName, numberOfElements=0, elementsOffset=0, AccessModeFlags=None):
        if userType is np.int32:
            accessor = self._device.getTwoDAccessor_int32(
                registerPathName, numberOfElements, elementsOffset)

        else:
            raise SyntaxError(
                "userType not supported"
            )

        # buffer = accessor.getBuffer()
        twoDRegisterAccessor = TwoDRegisterAccessor(userType, accessor)
        return twoDRegisterAccessor


class AccessMode(enum.Enum):
    raw = pb.AccessMode.raw
    wait_for_new_data = pb.AccessMode.wait_for_new_data


class TwoDRegisterAccessor(np.ndarray):

    def __new__(cls, userType, accessor):
        # add the new attribute to the created instance
        cls._accessor = accessor
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        channels = accessor.getNChannels()
        elementsPerChannel = accessor.getNElementsPerChannel()
        obj = np.asarray(
            np.zeros(shape=(channels, elementsPerChannel), dtype=userType)).view(cls)
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.info = getattr(obj, 'info', None)

    def read(self):
        self._accessor.read(self.view())

    def readLatest(self):
        return False

    def readNonBlocking(self):
        return False

    def write(self):
        self._accessor.write(self.view())

    def getNChannels(self):
        return self._accessor.getNChannels()

    def getNElementsPerChannel(self):
        return self._accessor.getNElementsPerChannel()
