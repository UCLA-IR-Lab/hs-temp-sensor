import argparse
from logging import basicConfig, StreamHandler, DEBUG, CRITICAL, ERROR, WARNING, INFO

from hs_temp_sensor import ad7124

def main() -> None:
    parser = argparse.ArgumentParser(description="HISPEC 4-wire Temperature Sensor Test Software")
    parser.add_argument("-v", "--verbose", dest="verbosity", action="count", default=0,
                        help="Verbosity (between 1-4 occurrences with more leading to more verbose logging)" \
                        "CRITICAL=0, ERROR=1, WARNING=2, INFO=3, DEBUG=4")
    parser.add_argument("-d", "--device", type=int, default="0", help="I2C device number (default: 0)")
    parser.add_argument("-r", "--reset", action="store_true", help="Reset the ADC chip")
    parser.add_argument("--id", action="store_true", help="Read chip ID")
    parser.add_argument("--temp", action="store_true", help="Read on-chip die temperature")
    parser.add_argument("--test", action="store_true", help="Run a test sequence")
    parser.add_argument("--rtd", action="store_true", help="RTD measurement")
    parser.add_argument("--sd", action="store_true", help="Silicon Diode measurement")
    
    log_levels = {
        0: CRITICAL,
        1: ERROR,
        2: WARNING,
        3: INFO,
        4: DEBUG
    }

    args = parser.parse_args()

    basicConfig(
        level=log_levels[min(args.verbosity, max(log_levels.keys()))],
        format='%(asctime)s %(name)s:%(lineno)s [%(levelname)s]: %(message)s'
    )

    print("Using SPI device: {}".format(args.device))
    
    adc = ad7124.AD7124(args.device)
    adc.connect()
    
    if args.reset:
        adc.reset()
        adc.close()
        
        return
    
    if args.id:
        id_reg, dev_id, silicon_rev = adc.read_id()
        adc.close()
        
        print("ADC Chip ID Register: 0x{:02X}".format(id_reg))
        print("ADC Chip ID: {}".format(dev_id))
        print("ADC Chip Silicon Revision: {}".format(silicon_rev))
        
        return
    
    if args.temp:
        adc.initialize()
        # if args.verbosity:
        #     adc.read_adc_config()
        #     adc.read_channel_config()
        #     adc.read_data()
        adc.set_adc_config()
        adc.set_config(gain=1, cfg_channel=0)
        adc.set_channel_config(channel=0, setup=0, ainp=16, ainm=17)
        # if args.verbosity:
        #     adc.read_adc_config()
        #     adc.read_channel_config()
        data, status = adc.read_data()
        adc.read_status()
        adc.set_channel_config(channel=0, disable=True)
        die_temp = adc.read_die_temp(data)
        adc.close()
        
        print("Die Temperature: {:.5f} °C".format(die_temp))
        print("Status Register: 0x{:02X}".format(status))
        
        return
    
    if args.test:
        if args.rtd:
            print("Running RTD test...")
            test_rtd(adc)
        elif args.sd:
            print("Running Silicon Diode test...")
            test_sd(adc)
        else:
            print("No test specified. Use --rtd or --sd for specific tests.")
            return
        
    adc.close()
    
    
def test_rtd(adc: ad7124.AD7124) -> None:
    adc.initialize()
        
    adc.set_adc_config()
    adc.set_config(gain=16, cfg_channel=0)
    
    adc.set_channel_config(channel=0, setup=0, ainp=16, ainm=17)
    ch0_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=0, disable=True)
    
    adc.set_io_control(iout0_ch=1, ex_cur=500, io_control=1)
    adc.set_channel_config(channel=1, setup=0, ainp=2, ainm=3)
    ch1_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=1, disable=True)
    
    adc.set_io_control(iout0_ch=4, ex_cur=500, io_control=1)
    adc.set_channel_config(channel=2, setup=0, ainp=5, ainm=6)
    ch2_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=2, disable=True)
    
    adc.set_io_control(iout0_ch=8, ex_cur=500, io_control=1)
    adc.set_channel_config(channel=3, setup=0, ainp=9, ainm=10)
    ch3_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=3, disable=True)
    
    adc.set_io_control(iout0_ch=11, ex_cur=500, io_control=1)
    adc.set_channel_config(channel=4, setup=0, ainp=12, ainm=13)
    ch4_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=4, disable=True)
        
    die_temp = adc.read_die_temp(ch0_data)
    # # adc.read_die_temp(ch1_data)
    # # adc.read_die_temp(ch2_data)
    res_a =  adc.rtd_test_conversion(ch1_data)
    res_b = adc.rtd_test_conversion(ch2_data)
    res_c = adc.rtd_test_conversion(ch3_data)
    res_d = adc.rtd_test_conversion(ch4_data)
    # # adc.rtd_test_conversion(ch5_data)
    # adc.read_die_temp(ch5_data)
    
    adc.reset()
    
    print("Die Temperature: {:.5f} °C".format(die_temp))
    print("RTD Channel A Resistance: {:.5f} Ohm".format(res_a))
    print("RTD Channel B Resistance: {:.5f} Ohm".format(res_b))
    print("RTD Channel C Resistance: {:.5f} Ohm".format(res_c))
    print("RTD Channel D Resistance: {:.5f} Ohm".format(res_d))
    
def test_sd(adc: ad7124.AD7124) -> None:
    adc.initialize()
        
    adc.set_adc_config()
    adc.set_config(gain=1, cfg_channel=0)
    adc.read_config()
    
    
    adc.set_channel_config(channel=0, setup=0, ainp=16, ainm=17)
    ch0_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=0, disable=True)
    
    adc.set_io_control(iout0_ch=1,  ex_cur=50, io_control=1)
    adc.set_channel_config(channel=1, setup=0, ainp=2, ainm=3)
    ch1_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=1, disable=True)
    
    adc.set_io_control(iout0_ch=4, ex_cur=50, io_control=1)
    adc.set_channel_config(channel=2, setup=0, ainp=5, ainm=6)
    ch2_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=2, disable=True)
    
    adc.set_io_control(iout0_ch=8, ex_cur=50, io_control=1)
    adc.set_channel_config(channel=3, setup=0, ainp=9, ainm=10)
    ch3_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=3, disable=True)
    
    adc.set_io_control(iout0_ch=11, ex_cur=50, io_control=1)
    adc.set_channel_config(channel=4, setup=0, ainp=12, ainm=13)
    ch4_data = adc.read_data()
    adc.read_status()
    adc.set_channel_config(channel=4, disable=True)
    
    die_temp = adc.read_die_temp(ch0_data)
    vol_e = adc.sd_test_conversion(ch1_data)
    vol_f = adc.sd_test_conversion(ch2_data)
    vol_g = adc.sd_test_conversion(ch3_data)
    vol_h = adc.sd_test_conversion(ch4_data)
    
    adc.reset()
    
    print("Die Temperature: {:.5f} °C".format(die_temp))
    print("SD Channel E Resistance: {:.5f} Ohm".format(vol_e))
    print("SD Channel F Resistance: {:.5f} Ohm".format(vol_f))
    print("SD Channel G Resistance: {:.5f} Ohm".format(vol_g))
    print("SD Channel H Resistance: {:.5f} Ohm".format(vol_h))
    
if __name__ == "__main__":
    main()