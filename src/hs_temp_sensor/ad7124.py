from logging import getLogger
import spidev
import time

logger = getLogger(__name__)

AD7124_SPI_BUS = 0
AD7124_SPI_DEVICE = 0
AD7124_SPI_MODE = 3
AD7124_SPI_MAX_SPEED = 1000000


AD7124_COMMS_REG = 0x00
AD7124_COMM_REG_WEN = 0 << 7
AD7124_COMM_REG_WR = 0 << 6
AD7124_COMM_REG_RD = 1 << 6
AD7124_COMM_REG_RA = lambda x : (x & 0x3F)

AD7124_STATUS_REG = 0x00

AD7124_ADC_CTRL_REG = 0x01
AD7124_ADC_CTRL_REG_DOUT_RDY_DEL = 1 << 12
AD7124_ADC_CTRL_REG_CONT_READ = 1 << 11
AD7124_ADC_CTRL_REG_DATA_STATUS = 1 << 10
AD7124_ADC_CTRL_REG_CS_EN = 1 << 9
AD7124_ADC_CTRL_REG_REF_EN = 1 << 8
AD7124_ADC_CTRL_REG_POWER_MODE = lambda x : (x & 0x03) << 6
AD7124_ADC_CTRL_REG_MODE = lambda x : (x & 0x0F) << 2
AD7124_ADC_CTRL_REG_CLK_SEL = lambda x : (x & 0x03)

AD7124_DATA_REG = 0x02

AD7124_IO_CTRL1_REG = 0x03
AD7124_IO_CTRL1_REG_GPIO_DAT4 = 1 << 23
AD7124_IO_CTRL1_REG_GPIO_DAT3 = 1 << 22
AD7124_IO_CTRL1_REG_GPIO_DAT2 = 1 << 21
AD7124_IO_CTRL1_REG_GPIO_DAT1 = 1 << 20
AD7124_IO_CTRL1_REG_GPIO_CTRL4 = 1 << 19
AD7124_IO_CTRL1_REG_GPIO_CTRL3 = 1 << 18
AD7124_IO_CTRL1_REG_GPIO_CTRL2 = 1 << 17
AD7124_IO_CTRL1_REG_GPIO_CTRL1 = 1 << 16
AD7124_IO_CTRL1_REG_PDSW = 1 << 15
AD7124_IO_CTRL1_REG_IOUT1 = lambda x : (x & 0x07) << 11
AD7124_IO_CTRL1_REG_IOUT0 = lambda x : (x & 0x07) << 8
AD7124_IO_CTRL1_REG_IOUT1_CH = lambda x : (x & 0x0F) << 4
AD7124_IO_CTRL1_REG_IOUT0_CH = lambda x : (x & 0x0F)

AD7124_IO_CTRL2_REG = 0x04

AD7124_ID_REG = 0x05
AD7124_ERR_REG = 0x06

AD7124_CH0_MAP_REG = 0x09
AD7124_CH1_MAP_REG = 0x0A
AD7124_CH2_MAP_REG = 0x0B
AD7124_CH3_MAP_REG = 0x0C
AD7124_CH4_MAP_REG = 0x0D
AD7124_CH5_MAP_REG = 0x0E
AD7124_CH6_MAP_REG = 0x0F
AD7124_CH7_MAP_REG = 0x10
AD7124_CH8_MAP_REG = 0x11
AD7124_CH9_MAP_REG = 0x12
AD7124_CH10_MAP_REG = 0x13
AD7124_CH11_MAP_REG = 0x14
AD7124_CH12_MAP_REG = 0x15
AD7124_CH13_MAP_REG = 0x16
AD7124_CH14_MAP_REG = 0x17
AD7124_CH15_MAP_REG = 0x18
AD7124_CH_MAP_REG_CH_ENABLE = 1 << 15
AD7124_CH_MAP_REG_CH_DISABLE = 0 << 15
AD7124_CH_MAP_REG_SETUP = lambda x : (x & 0x07) << 12
AD7124_CH_MAP_REG_AINP = lambda x : (x & 0x1F) << 5
AD7124_CH_MAP_REG_AINM = lambda x : (x & 0x1F)

AD7124_CFG0_REG = 0x19
AD7124_CFG_REG_BIPOLAR = 1 << 11
AD7124_CFG_REG_BURNOUT = lambda x : (x & 0x03) << 9
AD7124_CFG_REG_REF_BUFP = 1 << 8
AD7124_CFG_REG_REF_BUFM = 1 << 7
AD7124_CFG_REG_AIN_BUFP = 1 << 6
AD7124_CFG_REG_AIN_BUFM = 1 << 5
AD7124_CFG_REG_REF_SEL = lambda x : (x & 0x03) << 3
AD7124_CFG_REG_PGA = lambda x : (x & 0x07)


class AD7124:
    def __init__(self):
        self.spi = spidev.SpiDev()
        
    def connect(self):
        self.spi.open(AD7124_SPI_BUS, AD7124_SPI_DEVICE)
        self.spi.mode = AD7124_SPI_MODE
        self.spi.max_speed_hz = AD7124_SPI_MAX_SPEED
        
    def close(self):
        self.spi.close()
        
    def initialize(self):
        self.reset()
        
    def reset(self):
        self.spi.xfer2([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        logger.debug("Reset complete")
        
    def read_status(self):
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN | AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_STATUS_REG)
        response = self.spi.xfer2([comms_write, 0x00])
        status_register = response[-1] & 0xFF
        logger.debug("Status Register: 0x{:02X}".format(status_register))
        logger.debug("Channel {} Converted".format(status_register & 0x0F))
        
        return status_register
        
    def read_id(self):
        command = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_ID_REG)
        response = self.spi.xfer2([AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_ID_REG), 0x00])
        id_register = response[-1]
        device_id = (id_register >> 4) & 0x0F
        silicon_rev = id_register & 0x0F
        logger.info("ID Register: 0x{:02X}".format(id_register))
        logger.debug("Device ID: {}".format(device_id))
        logger.debug("Silicon Revision: {}".format(silicon_rev))
        
        return id_register, device_id, silicon_rev
    
    def configure(self):
        self.set_adc_config()
        self.set_channel_config()
        
    def set_config(self, cfg_channel=0):
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_WR | AD7124_COMM_REG_RA(AD7124_CFG0_REG)
        config_reg = AD7124_CFG_REG_BIPOLAR | AD7124_CFG_REG_AIN_BUFP | AD7124_CFG_REG_AIN_BUFM | AD7124_CFG_REG_REF_SEL(2) | AD7124_CFG_REG_PGA(5)
        self.spi.xfer2([comms_write, (config_reg >> 8) & 0xFF, config_reg & 0xFF])
        logger.debug("Configuration Register {} set to: 0x{:04X}".format(cfg_channel, config_reg))
        
    def read_config(self, cfg_channel=0):
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_CFG0_REG)
        response = self.spi.xfer2([comms_write, 0x00, 0x00])
        config_reg = (response[-2] << 8) | response[-1]
        logger.debug("Configuration Register {}: 0x{:04X}".format(cfg_channel, config_reg))
        
        return config_reg
    
    def set_adc_config(self):
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_WR | AD7124_COMM_REG_RA(AD7124_ADC_CTRL_REG)
        adc_config = AD7124_ADC_CTRL_REG_DOUT_RDY_DEL | AD7124_ADC_CTRL_REG_DATA_STATUS | AD7124_ADC_CTRL_REG_REF_EN | AD7124_ADC_CTRL_REG_POWER_MODE(3) | AD7124_ADC_CTRL_REG_MODE(0) | AD7124_ADC_CTRL_REG_CLK_SEL(0)
        # adc_config = AD7124_ADC_CTRL_REG_DOUT_RDY_DEL | AD7124_ADC_CTRL_REG_DATA_STATUS | AD7124_ADC_CTRL_REG_REF_EN | AD7124_ADC_CTRL_REG_POWER_MODE(3) | AD7124_ADC_CTRL_REG_MODE(1) | AD7124_ADC_CTRL_REG_CLK_SEL(0)
        self.spi.xfer2([comms_write, (adc_config >> 8) & 0xFF, adc_config & 0xFF])
        logger.debug("ADC Configured")
        
    def read_adc_config(self):
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_ADC_CTRL_REG)
        response = self.spi.xfer2([comms_write, 0x00, 0x00])
        adc_control_reg = response[-2] << 8 | response[-1]
        logger.debug("ADC Configuration: 0x{:04X}".format(adc_control_reg))
        
    def set_channel_config(self, channel=0, setup=0, ainp=16, ainm=17):
        channel_reg = self._channel_selector(channel)
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_WR | AD7124_COMM_REG_RA(channel_reg)
        channel_config = AD7124_CH_MAP_REG_CH_ENABLE | AD7124_CH_MAP_REG_SETUP(0) | AD7124_CH_MAP_REG_AINP(ainp) | AD7124_CH_MAP_REG_AINM(ainm)
        self.spi.xfer2([comms_write, (channel_config >> 8) & 0xFF, channel_config & 0xFF])
        logger.debug("Channel {} Configured: 0x{:04X}".format(channel, channel_config))
    
    def read_channel_config(self, channel=0):
        channel_reg = self._channel_selector(channel)
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(channel_reg)
        response = self.spi.xfer2([comms_write, 0x00, 0x00])
        channel_config_reg = response[-2] << 8 | response[-1]
        logger.debug("Channel {} Configuration: 0x{:04X}".format(channel, channel_config_reg))
        
    def read_data(self):
        time.sleep(0.1)
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN | AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_DATA_REG)
        data_reg = self.spi.xfer2([comms_write, 0x00, 0x00, 0x00])
        data = (data_reg[-3] << 16) | (data_reg[-2] << 8) | data_reg[-1]
        logger.debug("Data Register: 0x{:06X}".format(data))
        
        return data
    
    def read_die_temp(self, data):
        die_temp = ((data - 0x800000)/13584) - 272.5
        logger.info("Die Temperature: {:.5f} °C".format(die_temp))
        
        return die_temp
    
    def read_io_control(self, io_channel=1):
        match io_channel:
            case 1:
                comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_IO_CTRL1_REG)
            case 2:
                comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_IO_CTRL2_REG)
            case _:
                logger.error("Invalid IO channel specified")
                return None
        
        response = self.spi.xfer2([comms_write, 0x00, 0x00, 0x00])
        io_control_reg = (response[-3] << 16) | (response[-2] << 8) | response[-1]
        logger.info("IO Control {}: 0x{:06X}".format(io_channel, io_control_reg))
        
        return io_control_reg
    
    def set_io_control(self, io_channel=1):
        match io_channel:
            case 1:
                comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_WR | AD7124_COMM_REG_RA(AD7124_IO_CTRL1_REG)
            case 2:
                comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_WR | AD7124_COMM_REG_RA(AD7124_IO_CTRL2_REG)
            case _:
                logger.error("Invalid IO channel specified")
                return None
            
        io_control_config = AD7124_IO_CTRL1_REG_IOUT0(4) | AD7124_IO_CTRL1_REG_IOUT0_CH(0)
        self.spi.xfer2([comms_write, (io_control_config >> 16) & 0xFF, (io_control_config >> 8) & 0xFF, io_control_config & 0xFF])
        logger.debug("IO {} Configured: 0x{:04X}".format(io_channel, io_control_config))
        
    def test_conversion(self, data):
        resistor_rtd = (data * 5.11*10**3) / (32 * 2**23)
        logger.info("RTD Resistance: {:.2f} Ohms".format(resistor_rtd))
        
        return resistor_rtd
    
    def _channel_selector(self, channel):
        match channel:
            case 0:
                return AD7124_CH0_MAP_REG
            case 1:
                return AD7124_CH1_MAP_REG
            case 2:
                return AD7124_CH2_MAP_REG
            case 3:
                return AD7124_CH3_MAP_REG
            case 4:
                return AD7124_CH4_MAP_REG
            case 5:
                return AD7124_CH5_MAP_REG
            case 6:
                return AD7124_CH6_MAP_REG
            case 7:
                return AD7124_CH7_MAP_REG
            case 8:
                return AD7124_CH8_MAP_REG
            case 9:
                return AD7124_CH9_MAP_REG
            case 10:
                return AD7124_CH10_MAP_REG
            case 11:
                return AD7124_CH11_MAP_REG
            case 12:
                return AD7124_CH12_MAP_REG
            case 13:
                return AD7124_CH13_MAP_REG
            case 14:
                return AD7124_CH14_MAP_REG
            case 15:
                return AD7124_CH15_MAP_REG
            case _:
                logger.error("Invalid channel specified")
                return None
            