import spidev

AD7124_SPI_BUS = 0
AD7124_SPI_DEVICE = 0
AD7124_SPI_MODE = 3
AD7124_SPI_MAX_SPEED = 1000000


AD7124_COMMS_REG = 0x00
AD7124_COMM_REG_WEN = 0 << 7
AD7124_COMM_REG_WR = 0 << 6
AD7124_COMM_REG_RD = 1 << 6
AD7124_COMM_REG_RA = lambda x : (x & 0x3F)

AD7124_DATA_REG = 0x02

AD7124_ID_REG = 0x05
AD7124_ERR_REG = 0x06

AD7124_CH0_MAP_REG = 0x09
AD7124_CH_MAP_REG_CH_ENABLE = 1 << 15
AD7124_CH_MAP_REG_CH_DISABLE = 0 << 15
AD7124_CH_MAP_REG_SETUP = lambda x : (x & 0x07) << 12
AD7124_CH_MAP_REG_AINP = lambda x : (x & 0x1F) << 5
AD7124_CH_MAP_REG_AINN = lambda x : (x & 0x1F)

class AD7124:
    def __init__(self):
        self.spi = spidev.SpiDev()
        
    def connect(self):
        self.spi.open(AD7124_SPI_BUS, AD7124_SPI_DEVICE)
        self.spi.mode = AD7124_SPI_MODE
        self.spi.max_speed_hz = AD7124_SPI_MAX_SPEED
        
    def close(self):
        self.spi.close()
        
    def reset(self):
        self.spi.writebytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        print("Reset complete")
        
    def read_id(self):
        response = self.spi.xfer2([AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_ID_REG), 0x00])
        id_register = response[-1]
        device_id = (id_register >> 4) & 0x0F
        silicon_rev = id_register & 0x0F
        print("ID Register: 0x{:02X}".format(id_register))
        print("\tDevice ID: {}".format(device_id))
        print("\tSilicon Revision: {}".format(silicon_rev))
        
        return id_register, device_id, silicon_rev
    
    def read_die_temp(self):
        comms_write = AD7124_COMMS_REG | AD7124_COMM_REG_WEN| AD7124_COMM_REG_WR | AD7124_COMM_REG_RA(AD7124_CH0_MAP_REG)]
        set_ch0 = AD7124_CH_MAP_REG_CH_ENABLE | AD7124_CH_MAP_REG_SETUP(0) | AD7124_CH_MAP_REG_AINP(0x10) | AD7124_CH_MAP_REG_AINN(0x10)
        # response = self.spi.xfer2([(set_ch0 >> 8) & 0xFF, set_ch0 & 0xFF])
        # print(response)
        data_read = AD7124_COMMS_REG | AD7124_COMM_REG_WEN | AD7124_COMM_REG_RD | AD7124_COMM_REG_RA(AD7124_DATA_REG)
        response = self.spi.xfer2([comms_write, (set_ch0 >> 8) & 0xFF, set_ch0 & 0xFF, data_read, 0x00, 0x00, 0x00])
        print(response)
        die_temp = (response[1] << 8) | response[2]
        die_temp = (die_temp >> 4) & 0xFFF
        die_temp = (die_temp * 0.0625) - 273.15
        print("Die Temperature: {} °C".format(die_temp))
        
        return die_temp