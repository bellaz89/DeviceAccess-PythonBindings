#include "devBaseAdapter.h"

namespace mtca4upy {

devBaseAdapter::devBaseAdapter(mtca4u::devBase* mtcaDevice)
    : _mtcaDevice(mtcaDevice) {}

void devBaseAdapter::writeRaw(uint32_t regOffset,
                              bp::numeric::array dataToWrite,
                              size_t bytesToWrite, uint8_t bar) {
  throwExceptionIfOutOfBounds(dataToWrite, bytesToWrite);
  if (extractDataType(dataToWrite) == INT32) {
    int32_t* dataPointer =
        reinterpret_cast<int32_t*>(extractDataPointer(dataToWrite));
    _mtcaDevice->writeArea(regOffset, dataPointer, bytesToWrite, bar);
  } else {
    throw mtca4upy::ArrayElementTypeNotSupported(
        "Data format used is unsupported");
  }
}

boost::shared_ptr<mtca4u::devMap<mtca4u::devBase>::RegisterAccessor>
devBaseAdapter::getRegisterAccessor(const std::string& moduleName,
                                    const std::string& regName) {
  (void)(moduleName);
  (void)(regName);
  throw MethodNotImplementedException(
      "This method is not available for this device");
}

devBaseAdapter::~devBaseAdapter() {
  // TODO Auto-generated destructor stub
}

} /* namespace mtcapy */

boost::shared_ptr<mtca4u::MultiplexedDataAccessor<float> >
mtca4upy::devBaseAdapter::getMultiplexedDataAccessor(
    const std::string& /*moduleName*/, const std::string& /*regionName*/) {
  throw MethodNotImplementedException(
      "MultiplexedDataAccessor creation not supported for this device");
}
