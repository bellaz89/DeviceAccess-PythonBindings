#include "devMapAdapter.h"

namespace mtca4upy {

void devMapAdapter::readRaw(uint32_t regOffset, bp::numeric::array Buffer,
                            size_t size, uint8_t bar) {
  throwExceptionIfOutOfBounds(Buffer, size);
  _mappedDevice->readArea(regOffset, mtca4upy::extractDataPointer(Buffer), size, bar);
}

void devMapAdapter::writeRaw(uint32_t regOffset, bp::numeric::array dataToWrite,
                             size_t bytesToWrite, uint8_t bar) {
  throwExceptionIfOutOfBounds(dataToWrite, bytesToWrite);
  _mappedDevice->writeArea(regOffset, mtca4upy::extractDataPointer(dataToWrite),
                           bytesToWrite, bar);
}

void devMapAdapter::readDMA(uint32_t regOffset, bp::numeric::array Buffer,
                            size_t size) {
  uint8_t dummyDMABar = 0; // The value should not matter; MappedDevice readDMA
                           // would not be dependent on the pcie bar
  throwExceptionIfOutOfBounds(Buffer, size);
  _mappedDevice->readDMA(regOffset, mtca4upy::extractDataPointer(Buffer), size,
                         dummyDMABar);
}

void devMapAdapter::writeDMA(uint32_t regOffset, bp::numeric::array dataToWrite,
                             size_t bytesToWrite) {
  uint8_t dummyDMABar = 0;
  throwExceptionIfOutOfBounds(dataToWrite, bytesToWrite);
  _mappedDevice->writeDMA(regOffset, mtca4upy::extractDataPointer(dataToWrite),
                          bytesToWrite, dummyDMABar);
}

void devMapAdapter::readDMA(const std::string& regName,
                            bp::numeric::array bufferSpace, size_t dataSize,
                            uint32_t addRegOffset) {
  throwExceptionIfOutOfBounds(bufferSpace, dataSize);
  _mappedDevice->readDMA(regName, mtca4upy::extractDataPointer(bufferSpace), dataSize,
                         addRegOffset);
}

void devMapAdapter::writeDMA(const std::string& regName,
                             bp::numeric::array dataToWrite, size_t dataSize,
                             uint32_t addRegOffset) {
  throwExceptionIfOutOfBounds(dataToWrite, dataSize);
  _mappedDevice->writeDMA(regName, mtca4upy::extractDataPointer(dataToWrite), dataSize,
                          addRegOffset);
}

void devMapAdapter::readRaw(const std::string& regName,
                            bp::numeric::array Buffer, size_t dataSize,
                            uint32_t addRegOffset) {
  // if dataSize == 0 then we are supposed to read the whole register. In this
  // case find the size of the 'Buffer' parameter and use this size. This should
  // trigger a runtime error if the space of 'Buffer' is not enough to hold the
  // register content
  size_t bytesToRead = dataSize;
  if (dataSize == 0) {
    bytesToRead = mtca4upy::extractNumberOfElements(Buffer) * sizeof(int32_t);
  }
  throwExceptionIfOutOfBounds(Buffer, bytesToRead);
  _mappedDevice->readReg(regName, mtca4upy::extractDataPointer(Buffer), bytesToRead ,
                         addRegOffset);
}

void devMapAdapter::writeRaw(const std::string& regName,
                             bp::numeric::array Buffer, size_t dataSize,
                             uint32_t addRegOffset) {
  // if dataSize == 0 then we are supposed to write the whole register. In this
  // case find the size of the 'Buffer' parameter and use this size. This should
  // trigger a runtime error if the space of 'Buffer' is not enough to hold the
  // register content
  size_t bytesToWrite = dataSize;
  if (dataSize == 0) {
    bytesToWrite = mtca4upy::extractNumberOfElements(Buffer) * sizeof(int32_t);
  }
  throwExceptionIfOutOfBounds(Buffer, bytesToWrite);
  _mappedDevice->writeReg(regName, mtca4upy::extractDataPointer(Buffer), bytesToWrite, addRegOffset);

}

devMapAdapter::devMapAdapter(mtca4u::devMap<mtca4u::devBase>* mappedDevice)
    : _mappedDevice(mappedDevice) {}

  mtca4u::devMap<mtca4u::devBase>::RegisterAccessor
  devMapAdapter::getRegisterAccessor (const std::string& regName) {
    return(_mappedDevice->getRegisterAccessor(regName));
  }

devMapAdapter::~devMapAdapter() {
  // TODO Auto-generated destructor stub
}
} /* namespace mtcapy */
