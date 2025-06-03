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

    adc = ad7124.AD7124(args.device)
    adc.connect()
    
    if args.reset:
        adc.reset()
        adc.close()
        
        return
    
    if args.id:
        adc.read_id()
        adc.close()
        
        return
    
    if args.temp:
        adc.initialize()
        if args.verbosity:
            adc.read_adc_config()
            adc.read_channel_config()
            adc.read_data()
        adc.configure()
        if args.verbosity:
            adc.read_adc_config()
            adc.read_channel_config()
        data = adc.read_data()
        adc.read_die_temp(data)
        adc.close()
        
        return
    
    if args.test:
        if args.rtd:
            test_rtd(adc)
        elif args.sd:
            test_sd(adc)
        else:
            print("No test specified. Use --rtd or --sd for specific tests.")
            return
        
    adc.close()
    
    
def test_rtd(adc: ad7124.AD7124) -> None:
    adc.initialize()
        
    adc.set_adc_config()
    adc.set_config(gain=4, cfg_channel=0)
    
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
        
    adc.read_die_temp(ch0_data)
    # # adc.read_die_temp(ch1_data)
    # # adc.read_die_temp(ch2_data)
    adc.rtd_test_conversion(ch1_data)
    adc.rtd_test_conversion(ch2_data)
    adc.rtd_test_conversion(ch3_data)
    adc.rtd_test_conversion(ch4_data)
    # # adc.rtd_test_conversion(ch5_data)
    # adc.read_die_temp(ch5_data)
    adc.reset()
    
def test_sd(adc: ad7124.AD7124) -> None:
    adc.initialize()
        
    adc.set_adc_config()
    adc.read_config()
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
    
    adc.read_die_temp(ch0_data)
    adc.sd_test_conversion(ch1_data)
    
    adc.reset()
    
if __name__ == "__main__":
    main()