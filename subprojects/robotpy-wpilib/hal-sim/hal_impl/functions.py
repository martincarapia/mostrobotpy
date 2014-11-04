
from hal import constants
from . import types

import time
import threading

from .data import hal_data

#
# Misc constants
#

CTR_RxTimeout = 1
CTR_TxTimeout = 2
CTR_InvalidParamValue = 3
CTR_UnexpectedArbId = 4

NiFpga_Status_FifoTimeout = -50400
NiFpga_Status_TransferAborted = -50405
NiFpga_Status_MemoryFull = -52000
NiFpga_Status_SoftwareFault = -52003
NiFpga_Status_InvalidParameter = -52005
NiFpga_Status_ResourceNotFound = -52006
NiFpga_Status_ResourceNotInitialized = -52010
NiFpga_Status_HardwareFault = -52018
NiFpga_Status_IrqTimeout = -61060

ERR_CANSessionMux_InvalidBuffer = -44408
ERR_CANSessionMux_MessageNotFound = -44087
WARN_CANSessionMux_NoToken = 44087
ERR_CANSessionMux_NotAllowed = -44088
ERR_CANSessionMux_NotInitialized = -44089

SAMPLE_RATE_TOO_HIGH = 1001
VOLTAGE_OUT_OF_RANGE = 1002
LOOP_TIMING_ERROR = 1004
SPI_WRITE_NO_MOSI = 1012
SPI_READ_NO_MISO = 1013
SPI_READ_NO_DATA = 1014
INCOMPATIBLE_STATE = 1015
NO_AVAILABLE_RESOURCES = -1004
NULL_PARAMETER = -1005
ANALOG_TRIGGER_LIMIT_ORDER_ERROR = -1010
ANALOG_TRIGGER_PULSE_OUTPUT_ERROR = -1011
PARAMETER_OUT_OF_RANGE = -1028

#############################################################################
# Semaphore
#############################################################################

# constants
SEMAPHORE_Q_FIFO = 0x01
SEMAPHORE_Q_PRIORITY = 0x01
SEMAPHORE_DELETE_SAFE = 0x04
SEMAPHORE_INVERSION_SAFE = 0x08
SEMAPHORE_NO_WAIT = 0
SEMAPHORE_WAIT_FOREVER = -1
SEMAPHORE_EMPTY = 0
SEMAPHORE_FULL = 1

def initializeMutexRecursive():
    return types.MUTEX_ID(threading.RLock())

def initializeMutexNormal():
    return types.MUTEX_ID(threading.Lock())

def deleteMutex(sem):
    sem.lock = None

def takeMutex(sem):
    sem.lock.acquire()
    return 0

def tryTakeMutex(sem):
    if not sem.lock.acquire(False):
        return -1
    return 0

def giveMutex(sem):
    sem.lock.release()
    return 0

def initializeSemaphore(initial_value):
    return types.SEMAPHORE_ID(threading.Semaphore(initial_value))

def deleteSemaphore(sem):
    sem.sem = None

def takeSemaphore(sem):
    sem.sem.acquire()

def tryTakeSemaphore(sem):
    if not sem.sem.acquire(False):
        return -1
    return 0

def giveSemaphore(sem):
    sem.sem.release()

def initializeMultiWait():
    return types.MULTIWAIT_ID(threading.Condition())

def deleteMultiWait(sem):
    sem.cond = None

def takeMultiWait(sem, timeout):
    sem.cond.wait() # timeout is ignored in C++ HAL

def giveMultiWait(sem):
    sem.cond.notifyAll() # hal uses pthread_cond_broadcast, which wakes all threads


#############################################################################
# HAL
#############################################################################

def getPort(pin):
    return getPortWithModule(0, pin)

def getPortWithModule(module, pin):
    return types.Port(pin, module)

def getHALErrorMessage(code):
    if code == 0:
        return ''

    elif code == CTR_RxTimeout:
        return "CTRE CAN Recieve Timeout"
    elif code == CTR_InvalidParamValue:
        return "CTRE CAN Invalid Parameter"
    elif code == CTR_UnexpectedArbId:
        return "CTRE Unexpected Arbitration ID (CAN Node ID)"
    elif code == NiFpga_Status_FifoTimeout:
        return "NIFPGA: FIFO timeout error"
    elif code == NiFpga_Status_TransferAborted:
        return "NIFPGA: Transfer aborted error"
    elif code == NiFpga_Status_MemoryFull:
        return "NIFPGA: Memory Allocation failed, memory full"
    elif code == NiFpga_Status_SoftwareFault:
        return "NIFPGA: Unexepected software error"
    elif code == NiFpga_Status_InvalidParameter:
        return "NIFPGA: Invalid Parameter"
    elif code == NiFpga_Status_ResourceNotFound:
        return "NIFPGA: Resource not found"
    elif code == NiFpga_Status_ResourceNotInitialized:
        return "NIFPGA: Resource not initialized"
    elif code == NiFpga_Status_HardwareFault:
        return "NIFPGA: Hardware Fault"
    elif code == NiFpga_Status_IrqTimeout:
        return "NIFPGA: Interrupt timeout"

    elif code == ERR_CANSessionMux_InvalidBuffer:
        return "CAN: Invalid Buffer"
    elif code == ERR_CANSessionMux_MessageNotFound:
        return "CAN: Message not found"
    elif code == WARN_CANSessionMux_NoToken:
        return "CAN: No token"
    elif code == ERR_CANSessionMux_NotAllowed:
        return "CAN: Not allowed"
    elif code == ERR_CANSessionMux_NotInitialized:
        return "CAN: Not initialized"

    elif code == SAMPLE_RATE_TOO_HIGH:
        return "HAL: Analog module sample rate is too high"
    elif code == VOLTAGE_OUT_OF_RANGE:
        return "HAL: Voltage to convert to raw value is out of range [0; 5]"
    elif code == LOOP_TIMING_ERROR:
        return "HAL: Digital module loop timing is not the expected value"
    elif code == SPI_WRITE_NO_MOSI:
        return "HAL: Cannot write to SPI port with no MOSI output"
    elif code == SPI_READ_NO_MISO:
        return "HAL: Cannot read from SPI port with no MISO input"
    elif code == SPI_READ_NO_DATA:
        return "HAL: No data available to read from SPI"
    elif code == INCOMPATIBLE_STATE:
        return "HAL: Incompatible State: The operation cannot be completed"
    elif code == NO_AVAILABLE_RESOURCES:
        return "HAL: No available resources to allocate"
    elif code == NULL_PARAMETER:
        return "HAL: A pointer parameter to a method is NULL"
    elif code == ANALOG_TRIGGER_LIMIT_ORDER_ERROR:
        return "HAL: AnalogTrigger limits error.  Lower limit > Upper Limit"
    elif code == ANALOG_TRIGGER_PULSE_OUTPUT_ERROR:
        return "HAL: Attempted to read AnalogTrigger pulse output."
    elif code == PARAMETER_OUT_OF_RANGE:
        return "HAL: A parameter is out of range."

    else:
        return "Unknown error status"

def getFPGAVersion(status):
    status.value = 0
    return 2015

def getFPGARevision(status):
    status.value = 0
    return 0

def getFPGATime(status):
    status.value = 0
    return int((time.monotonic() - hal_data['program_time']) * 100000)

def getFPGAButton(status):
    status.value = 0
    return hal_data['fpga_button']

def HALSetErrorData(errors, errorsLength, wait_ms):
    hal_data['error_data'] = errors

def HALGetControlWord():
    return types.HALControlWord(hal_data['control'])

def HALGetAllianceStation():
    return hal_data['alliance_station']

def HALGetJoystickAxes(joystickNum, axes):
    # we store as -1 to 1 for ease of use, so convert to -128 to 127 here
    return [int(a*128) if a < 0 else int(a*127) for a in hal_data['joysticks'][joystickNum]['axes']]

def HALGetJoystickPOVs(joystickNum, povs):
    return map(int, hal_data['joysticks'][joystickNum]['povs'][:])

def HALGetJoystickButtons(joystickNum, buttons, count):
    # buttons are stored as booleans for ease of use, convert to integer
    b = hal_data['joysticks'][joystickNum]['buttons']
    buttons.value = sum(int(v) << i for i, v in enumerate(b[1:]))
    buttons.count = len(b)-1

def HALSetNewDataSem(sem):
    pass

def HALInitialize(mode=0):
    pass

def HALNetworkCommunicationObserveUserProgramStarting():
    hal_data['user_program_state'] = 'starting'

def HALNetworkCommunicationObserveUserProgramDisabled():
    hal_data['user_program_state'] = 'disabled'

def HALNetworkCommunicationObserveUserProgramAutonomous():
    hal_data['user_program_state'] = 'autonomous'

def HALNetworkCommunicationObserveUserProgramTeleop():
    hal_data['user_program_state'] = 'teleop'

def HALNetworkCommunicationObserveUserProgramTest():
    hal_data['user_program_state'] = 'test'

def HALReport(resource, instanceNumber, context=0, feature=None):
    pass


#############################################################################
# Accelerometer
#############################################################################

def setAccelerometerActive(active):
    hal_data['accelerometer']['active'] = active

def setAccelerometerRange(range):
    hal_data['accelerometer']['range'] = range

def getAccelerometerX():
    return hal_data['accelerometer']['x']

def getAccelerometerY():
    return hal_data['accelerometer']['y']

def getAccelerometerZ():
    return hal_data['accelerometer']['z']


#############################################################################
# Analog
#############################################################################

kTimebase = 40000000 #< 40 MHz clock
kDefaultOversampleBits = 0
kDefaultAverageBits = 7
kDefaultSampleRate = 50000.0
kAnalogInputPins = 8
kAnalogOutputPins = 2

kAccumulatorNumChannels = 2
kAccumulatorChannels = [0, 1]

def _checkAnalogIsFree(port):
    if port.pin < kAnalogOutputPins:
        assert hal_data['analog_out'][port.pin]['initialized'] == False
    assert hal_data['analog_in'][port.pin]['initialized'] == False
    assert hal_data['analog_trigger'][port.pin]['initialized'] == False

def initializeAnalogOutputPort(port, status):
    _checkAnalogIsFree(port)
    status.value = 0
    hal_data['analog_out'][port.pin]['initialized'] = True
    return types.AnalogPort(port)

def setAnalogOutput(analog_port, voltage, status):
    status.value = 0
    hal_data['analog_out'][analog_port.pin]['output'] = voltage

def getAnalogOutput(analog_port, status):
    status.value = 0
    return hal_data['analog_out'][analog_port.pin]['output']

def checkAnalogOutputChannel(pin):
    return pin < kAnalogOutputPins

def initializeAnalogInputPort(port, status):
    _checkAnalogIsFree(port)
    status.value = 0
    #assert hal_data['analog_out'][port.pin] is None
    #assert hal_data['analog_trigger'][port.pin] is
    hal_data['analog_in']['initialized'] = True
    return types.AnalogPort(port)

def checkAnalogModule(module):
    return module == 1

def checkAnalogInputChannel(pin):
    return pin < kAnalogInputPins

def setAnalogSampleRate(samples_per_second, status):
    status.value = 0
    hal_data['analog_sample_rate'] = samples_per_second

def getAnalogSampleRate(status):
    status.value = 0
    return hal_data['analog_sample_rate']

def setAnalogAverageBits(analog_port, bits, status):
    status.value = 0
    hal_data['analog_in'][analog_port.pin]['avg_bits'] = bits

def getAnalogAverageBits(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['avg_bits']

def setAnalogOversampleBits(analog_port, bits, status):
    status.value = 0
    hal_data['analog_in'][analog_port.pin]['oversample_bits'] = bits

def getAnalogOversampleBits(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['oversample_bits']

def getAnalogValue(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['value']

def getAnalogAverageValue(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['avg_value']

def getAnalogVoltsToValue(analog_port, voltage, status):
    status.value = 0
    if voltage > 5.0:
        voltage = 5.0
        status.value = VOLTAGE_OUT_OF_RANGE
    elif voltage < 0.0:
        voltage = 0.0
        status.value = VOLTAGE_OUT_OF_RANGE

    LSBWeight = getAnalogLSBWeight(analog_port, status)
    offset = getAnalogOffset(analog_port, status)
    return (int)((voltage + offset * 1.0e-9) / (LSBWeight * 1.0e-9))

def getAnalogVoltage(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['voltage']

def getAnalogAverageVoltage(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['avg_voltage']

def getAnalogLSBWeight(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['lsb_weight']

def getAnalogOffset(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['offset']

def isAccumulatorChannel(analog_port, status):
    status.value = 0
    return analog_port.pin in kAccumulatorChannels

def initAccumulator(analog_port, status):
    status.value = 0
    hal_data['analog_in'][analog_port.pin]['accumulator_initialized'] = True

def resetAccumulator(analog_port, status):
    status.value = 0
    hal_data['analog_in'][analog_port.pin]['accumulator_center'] = 0
    hal_data['analog_in'][analog_port.pin]['accumulator_count'] = 0
    hal_data['analog_in'][analog_port.pin]['accumulator_value'] = 0

def setAccumulatorCenter(analog_port, center, status):
    status.value = 0
    hal_data['analog_in'][analog_port.pin]['accumulator_center'] = center

def setAccumulatorDeadband(analog_port, deadband, status):
    status.value = 0
    hal_data['analog_in'][analog_port.pin]['accumulator_deadband'] = deadband

def getAccumulatorValue(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['accumulator_value']

def getAccumulatorCount(analog_port, status):
    status.value = 0
    return hal_data['analog_in'][analog_port.pin]['accumulator_count']

def getAccumulatorOutput(analog_port, status):
    status.value = 0
    return (hal_data['analog_in'][analog_port.pin]['accumulator_value'],
           hal_data['analog_in'][analog_port.pin]['accumulator_count'])

def initializeAnalogTrigger(port, status):
    _checkAnalogIsFree(port)
    status.value = 0

def cleanAnalogTrigger(analog_trigger, status):
    assert False

def setAnalogTriggerLimitsRaw(analog_trigger, lower, upper, status):
    assert False

def setAnalogTriggerLimitsVoltage(analog_trigger, lower, upper, status):
    assert False

def setAnalogTriggerAveraged(analog_trigger, use_averaged_value, status):
    assert False

def setAnalogTriggerFiltered(analog_trigger, use_filtered_value, status):
    assert False

def getAnalogTriggerInWindow(analog_trigger, status):
    assert False

def getAnalogTriggerTriggerState(analog_trigger, status):
    assert False

def getAnalogTriggerOutput(analog_trigger, type, status):
    assert False


#############################################################################
# Compressor
#############################################################################

def initializeCompressor(module):
    assert module == 0 # don't support multiple modules for now
    hal_data['compressor'] = dict(enabled=True)
    return types.PCM(module)

def checkCompressorModule(module):
    return module < 63

def getCompressor(pcm, status):
    status.value = 0
    return hal_data['compressor']['enabled']

def setClosedLoopControl(pcm, value, status):
    status.value = 0
    hal_data['compressor']['closed_loop_enabled'] = value

def getClosedLoopControl(pcm, status):
    status.value = 0
    return hal_data['compressor']['closed_loop_enabled']

def getPressureSwitch(pcm, status):
    status.value = 0
    return hal_data['compressor']['pressure_switch']

def getCompressorCurrent(pcm, status):
    status.value = 0
    return hal_data['compressor']['current']


#############################################################################
# Digital
#############################################################################

kExpectedLoopTiming = 40
kDigitalPins = 26
kPwmPins = 20
kRelayPins = 8
kNumHeaders = 10

def initializeDigitalPort(port, status):
    status.value = 0
    return types.DigitalPort(port)

def checkPWMChannel(digital_port):
    return digital_port.pin < kPwmPins

def checkRelayChannel(digital_port):
    return digital_port.pin < kRelayPins

def setPWM(digital_port, value, status):
    assert False

def allocatePWMChannel(digital_port, status):
    status.value = 0

def freePWMChannel(digital_port, status):
    status.value = 0

def getPWM(digital_port, status):
    assert False

def latchPWMZero(digital_port, status):
    assert False

def setPWMPeriodScale(digital_port, squelch_mask, status):
    assert False

def allocatePWM(status):
    assert False

def freePWM(pwm, status):
    assert False

def setPWMRate(rate, status):
    assert False

def setPWMDutyCycle(pwm, duty_cycle, status):
    assert False

def setPWMOutputChannel(pwm, pin, status):
    assert False

def setRelayForward(digital_port, on, status):
    assert False

def setRelayReverse(digital_port, on, status):
    assert False

def getRelayForward(digital_port, status):
    assert False

def getRelayReverse(digital_port, status):
    assert False

def allocateDIO(digital_port, input, status):
    assert False

def freeDIO(digital_port, status):
    assert False

def setDIO(digital_port, value, status):
    assert False

def getDIO(digital_port, status):
    assert False

def getDIODirection(digital_port, status):
    assert False

def pulse(digital_port, pulse_length, status):
    assert False

def isPulsing(digital_port, status):
    assert False

def isAnyPulsing(status):
    assert False

def initializeCounter(mode, status):
    assert False

def freeCounter(counter, status):
    assert False

def setCounterAverageSize(counter, size, status):
    assert False

def setCounterUpSource(counter, pin, analog_trigger, status):
    assert False

def setCounterUpSourceEdge(counter, rising_edge, falling_edge, status):
    assert False

def clearCounterUpSource(counter, status):
    assert False

def setCounterDownSource(counter, pin, analog_trigger, status):
    assert False

def setCounterDownSourceEdge(counter, rising_edge, falling_edge, status):
    assert False

def clearCounterDownSource(counter, status):
    assert False

def setCounterUpDownMode(counter, status):
    assert False

def setCounterExternalDirectionMode(counter, status):
    assert False

def setCounterSemiPeriodMode(counter, high_semi_period, status):
    assert False

def setCounterPulseLengthMode(counter, threshold, status):
    assert False

def getCounterSamplesToAverage(counter, status):
    assert False

def setCounterSamplesToAverage(counter, samples_to_average, status):
    assert False

def resetCounter(counter, status):
    assert False

def getCounter(counter, status):
    assert False

def getCounterPeriod(counter, status):
    assert False

def setCounterMaxPeriod(counter, max_period, status):
    assert False

def setCounterUpdateWhenEmpty(counter, enabled, status):
    assert False

def getCounterStopped(counter, status):
    assert False

def getCounterDirection(counter, status):
    assert False

def setCounterReverseDirection(counter, reverse_direction, status):
    assert False

def initializeEncoder(port_a_module, port_a_pin, port_a_analog_trigger, port_b_module, port_b_pin, port_b_analog_trigger, reverse_direction, status):
    assert False

def freeEncoder(encoder, status):
    assert False

def resetEncoder(encoder, status):
    assert False

def getEncoder(encoder, status):
    assert False

def getEncoderPeriod(encoder, status):
    assert False

def setEncoderMaxPeriod(encoder, max_period, status):
    assert False

def getEncoderStopped(encoder, status):
    assert False

def getEncoderDirection(encoder, status):
    assert False

def setEncoderReverseDirection(encoder, reverse_direction, status):
    assert False

def setEncoderSamplesToAverage(encoder, samples_to_average, status):
    assert False

def getEncoderSamplesToAverage(encoder, status):
    assert False

def getLoopTiming(status):
    assert False

def spiInitialize(port, status):
    assert False

def spiTransaction(port, data_to_send, data_received, size):
    assert False

def spiWrite(port, data_to_send, send_size):
    assert False

def spiRead(port, buffer, count):
    assert False

def spiClose(port):
    assert False

def spiSetSpeed(port, speed):
    assert False

def spiSetOpts(port, msb_first, sample_on_trailing, clk_idle_high):
    assert False

def spiSetChipSelectActiveHigh(port, status):
    assert False

def spiSetChipSelectActiveLow(port, status):
    assert False

def spiGetHandle(port):
    assert False

def spiSetHandle(port, handle):
    assert False

def spiGetSemaphore(port):
    assert False

def spiSetSemaphore(port, semaphore):
    assert False

def i2CInitialize(port, status):
    assert False

def i2CTransaction(port, device_address, data_to_send, send_size, data_received, receive_size):
    assert False

def i2CWrite(port, device_address, data_to_send, send_size):
    assert False

def i2CRead(port, device_address, buffer, count):
    assert False

def i2CClose(port):
    assert False


#############################################################################
# Interrupts
#############################################################################

def initializeInterrupts(interrupt_index, watcher, status):
    assert False # TODO

def cleanInterrupts(interrupt, status):
    assert False # TODO

def waitForInterrupt(interrupt, timeout, ignorePrevious, status):
    assert False # TODO

def enableInterrupts(interrupt, status):
    assert False # TODO

def disableInterrupts(interrupt, status):
    assert False # TODO

def readRisingTimestamp(interrupt, status):
    assert False # TODO

def readFallingTimestamp(interrupt, status):
    assert False # TODO

def requestInterrupts(interrupt, routing_module, routing_pin, routing_analog_trigger, status):
    assert False # TODO

def attachInterruptHandler(interrupt, handler, param, status):
    assert False # TODO

def setInterruptUpSourceEdge(interrupt, rising_edge, falling_edge, status):
    assert False # TODO


#############################################################################
# Notifier
#############################################################################

def initializeNotifier(processQueue, status):
    assert False # TODO

def cleanNotifier(notifier, status):
    assert False # TODO

def updateNotifierAlarm(notifier, triggerTime, status):
    assert False # TODO


#############################################################################
# PDP
#############################################################################

def getPDPTemperature(status):
    status.value = 0
    return hal_data['pdp']['temperature']

def getPDPVoltage(status):
    status.value = 0
    return hal_data['pdp']['voltage']

def getPDPChannelCurrent(channel, status):
    if channel < 0 or channel >= len(hal_data['pdp']['current']):
        status.value = CTR_InvalidParamValue
        return 0
    status.value = 0
    return hal_data['pdp']['current'][channel]


#############################################################################
# Power
#############################################################################

def getVinVoltage(status):
    status.value = 0
    return hal_data['power']['vin_voltage']

def getVinCurrent(status):
    status.value = 0
    return hal_data['power']['vin_current']

def getUserVoltage6V(status):
    status.value = 0
    return hal_data['power']['user_voltage_6v']

def getUserCurrent6V(status):
    status.value = 0
    return hal_data['power']['user_current_6v']

def getUserVoltage5V(status):
    status.value = 0
    return hal_data['power']['user_voltage_5v']

def getUserCurrent5V(status):
    status.value = 0
    return hal_data['power']['user_current_5v']

def getUserVoltage3V3(status):
    status.value = 0
    return hal_data['power']['user_voltage_3v3']

def getUserCurrent3V3(status):
    status.value = 0
    return hal_data['power']['user_current_3v3']

#############################################################################
# Solenoid
#############################################################################

def initializeSolenoidPort(port, status):
    status.value = 0
    # sigh: it would be nice if all the solenoids weren't always initialized
    hal_data['solenoid'][port.pin] = False 
    return types.SolenoidPort(port)

def checkSolenoidModule(module):
    return module < 63

def getSolenoid(solenoid_port, status):
    status.value = 0
    return hal_data['solenoid'][solenoid_port.pin]

def setSolenoid(solenoid_port, value, status):
    status.value = 0
    hal_data['solenoid'][solenoid_port.pin] = value


#############################################################################
# Utilities
#############################################################################

HAL_NO_WAIT = 0
HAL_WAIT_FOREVER = -1

def delayTicks(ticks):
    # ticks is ns*3? don't use this.
    assert False

def delayMillis(ms):
    time.sleep(1000*ms)

def delaySeconds(s):
    time.sleep(s)

#############################################################################
# CAN
#############################################################################

def FRC_NetworkCommunication_CANSessionMux_sendMessage(messageID, data, dataSize, periodMs, status):
    assert False

def FRC_NetworkCommunication_CANSessionMux_receiveMessage(messageID, messageIDMask, data, status):
    assert False # returns dataSize, timeStamp

def FRC_NetworkCommunication_CANSessionMux_openStreamSession(messageID, messageIDMask, maxMessages, status):
    assert False # returns sessionHandle

def FRC_NetworkCommunication_CANSessionMux_closeStreamSession(sessionHandle):
    assert False

def FRC_NetworkCommunication_CANSessionMux_readStreamSession(sessionHandle, messages, messagesToRead, status):
    assert False # returns messagesRead

def FRC_NetworkCommunication_CANSessionMux_getCANStatus(status):
    assert False # returns all params

