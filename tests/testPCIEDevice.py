#! /usr/bin/python
import os
import sys
import  unittest
import numpy

# This is a hack for nw
sys.path.insert(0,os.path.abspath(os.curdir))
import mtcamappeddevice

class TestPCIEDevice(unittest.TestCase):

    def testCreatePCIEDevice(self):
        self.assertRaisesRegexp(RuntimeError, "Cannot open device: : No such "
                "file or directory", mtcamappeddevice.createDevice, "")
        self.assertRaisesRegexp(RuntimeError, "Cannot open device: "
                "some_non_existent_device: No such file or directory", mtcamappeddevice.createDevice,
                "some_non_existent_device")

    def testReadArea(self):
        device = mtcamappeddevice.createDevice("/dev/llrfdummys4")
        wordCompilationRegOffset = 4
        preAllocatedArray = numpy.zeros(2, dtype = numpy.int32)
        bytesToRead = 12
        registerBar = 0

        self.assertRaisesRegexp(RuntimeError, "size to write is more than the "
        "supplied array size", device.readArea, wordCompilationRegOffset,
        preAllocatedArray, bytesToRead, registerBar)


        badRegOffset = 563
        bytesToRead = 8

        self.assertRaisesRegexp(RuntimeError, "Cannot read data from device: "
        "/dev/llrfdummys4: Bad address", device.readArea, badRegOffset,
        preAllocatedArray, bytesToRead, registerBar)


        # read in th default value from WORD_FIRMWARE register
        wordCompilationRegOffset = 4
        bytesToRead = 4

        device.readArea(wordCompilationRegOffset, preAllocatedArray, bytesToRead,
                registerBar)
        self.assertTrue( 9 == preAllocatedArray[0])


        wordStatusRegOffset = 8
        dataArray = numpy.array([5, 9], dtype=numpy.int32)
        readInArray = numpy.zeros(2, dtype = numpy.int32)
        bytesToWrite = 8
        bytesToRead = 8

        device.writeArea(wordStatusRegOffset, dataArray,
                bytesToWrite, registerBar)
        device.readArea(wordStatusRegOffset, readInArray, bytesToRead,
                registerBar)

        self.assertTrue(readInArray.tolist() == dataArray.tolist())

    def testWriteArea(self):
        device = mtcamappeddevice.createDevice("/dev/llrfdummys4")
        wordStatusRegOffset = 8
        infoToWrite = numpy.array([566,58], dtype = numpy.int32)
        bytesToWrite = 12
        registerBar = 0


        self.assertRaisesRegexp(RuntimeError, "size to write is more than the "
        "supplied array size", device.writeArea, wordStatusRegOffset,
        infoToWrite, bytesToWrite, registerBar)
        
        badRegOffset = 5654
        bytesToWrite = 8
        
        self.assertRaisesRegexp(RuntimeError, "Cannot read data from device: "
        "/dev/llrfdummys4: Bad address", device.readArea, badRegOffset,
        infoToWrite, bytesToWrite, registerBar)

        # test of write done in the above testcase TODO: make this proper

    def testReadDMA(self):
        device = mtcamappeddevice.createDevice("/dev/llrfdummys4")
        # Set the WORD_ADC_ENA reg to 1; This sets the first 25 words of the
        # DMA memory area to a prabolically increasing set of values; The offset
        # for the WORD_ADC_ENA register is 68

        wordAdcEnaRegOffset = 68
        bytesToWrite = 4 # i.e one word
        registerBar = 0
        dataArray = numpy.array([1], dtype = numpy.int32)
        device.writeArea(wordAdcEnaRegOffset, dataArray, bytesToWrite,
               registerBar) # the DMA area would be set after this

         # TODO: Use a ;loop later
        expectedDataArray = numpy.array([0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100,
            121, 144, 169, 196, 225, 256,  289, 324, 361, 400, 441, 484, 529,
            576], dtype = numpy.int32)


        # read the DMA area which has been set with values
        dmaArea = 0
        readInArray = numpy.zeros(25, dtype = numpy.int32)
        bytesToRead = 25 * 4 # 25 words

        device.readDMA(dmaArea, readInArray, bytesToRead)

        self.assertTrue(readInArray.tolist() == expectedDataArray.tolist())




    def testWriteDMA(self):
        device = mtcamappeddevice.createDevice("/dev/llrfdummys4") 
        #TODO: Use loop later
        #dataToWrite = numpy.array([576, 529, 484, 441, 400, 361, 324, 289, 256,
            #225, 196, 169, 144, 121, 100, 81, 64, 49, 36, 25, 16, 9, 4, 1, 0],
            #dtype = numpy.int32)
        #dmaAreaAddress = 0
        #bytesToWrite = 25 * 4 # 25 entries inside dataToWrite
        #device.writeDMA(dmaAreaAddress, dataToWrite, bytesToWrite)

        #dataToRead = numpy.zeros(25, dtype = numpy.int32) # Space for content to read from
                                                          # DMA Area
        #bytesToRead = 25*4
        #device.readDMA(dmaAreaAddress, dataToRead, bytesToRead)

        #self.assertTrue(dataToRead.tolist() == dataToWrite.tolist())

        dmaAreaAddress = 0
        dataToWrite = numpy.array([1,2], dtype = numpy.int32)
        bytesToWrite = 2*4
        self.assertRaisesRegexp(RuntimeError, "Operation not supported yet",
                device.writeDMA, dmaAreaAddress, dataToWrite, bytesToWrite)
       

    #def testReadDMAThroughRegisterName():
        #device = mtcamappeddevice.createDevice("/dev/llrfdummys4")           
        #registerName = "WORD_ADC_ENA"
        #dataArray = numpy.zeros(1, dtype = numpy.int32)
#
        #device.


if __name__ == '__main__':
    unittest.main()
