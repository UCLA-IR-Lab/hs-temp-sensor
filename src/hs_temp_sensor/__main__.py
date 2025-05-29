import argparse
from logging import basicConfig, StreamHandler, DEBUG, CRITICAL, ERROR, WARNING, INFO

from hs_temp_sensor import ad7124

def main() -> None:
    parser = argparse.ArgumentParser(description="HISPEC 4-wire Temperature Sensor Test Software")
    parser.add_argument("-v", "--verbose", dest="verbosity", action="count", default=0,
                        help="Verbosity (between 1-4 occurrences with more leading to more verbose logging)" \
                        "CRITICAL=0, ERROR=1, WARNING=2, INFO=3, DEBUG=4")
    parser.add_argument("-r", "--reset", action="store_true", help="Reset the ADC chip")
    parser.add_argument("--id", action="store_true", help="Read chip ID")
    parser.add_argument("--temp", action="store_true", help="Read on-chip die temperature")
    parser.add_argument("--test", action="store_true", help="Run a test sequence")
    
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

    adc = ad7124.AD7124()
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
        adc.initialize()
        # for i in range(16):
        #     adc.read_channel_config(i)
        adc.read_status()
        adc.read_adc_config()
        adc.read_config(cfg_channel=0)
        adc.read_channel_config(0)
        adc.read_channel_config(1)
        adc.read_channel_config(2)
        adc.read_channel_config(3)
        adc.read_channel_config(4)
        adc.read_channel_config(5)
        adc.read_io_control(io_channel=1)
        
        
        adc.set_adc_config()
        adc.set_config(cfg_channel=0)
        # adc.set_channel_config(channel=0, setup=0, ainp=16, ainm=17)
        # adc.set_channel_config(channel=1, setup=0, ainp=2, ainm=3)
        # adc.set_channel_config(channel=2, setup=0, ainp=5, ainm=6)
        adc.set_channel_config(channel=3, setup=0, ainp=9, ainm=10)
        # adc.set_channel_config(channel=4, setup=0, ainp=12, ainm=13)
        # adc.set_channel_config(channel=5, setup=0, ainp=16, ainm=17)
        # adc.set_channel_config(channel=6, setup=0, ainp=16, ainm=17)
        # adc.set_channel_config(channel=7, setup=0, ainp=16, ainm=17)
        # adc.set_channel_config(channel=8, setup=0, ainp=16, ainm=17)
        # adc.set_channel_config(channel=9, setup=0, ainp=16, ainm=17)
        # adc.set_channel_config(channel=10, setup=0, ainp=16, ainm=17)
        # adc.set_channel_config(channel=11, setup=0, ainp=16, ainm=17)
        # adc.set_channel_config(channel=12, setup=0, ainp=16, ainm=17)
        adc.set_io_control(io_channel=1)
        # for i in range(16):
        #     adc.read_channel_config(i)
        
        adc.read_adc_config()
        adc.read_config(cfg_channel=0)
        adc.read_channel_config(0)
        adc.read_channel_config(1)
        adc.read_channel_config(2)
        adc.read_channel_config(3)
        adc.read_channel_config(4)
        adc.read_channel_config(5)
        adc.read_io_control(io_channel=1)

        for i in range(16):
            data = adc.read_data()
            adc.read_status()
            adc.read_die_temp(data)
            adc.test_conversion(data)
            
        # ch0_data = adc.read_data()
        # adc.read_status()
        # ch1_data = adc.read_data()
        # adc.read_status()
        # ch2_data = adc.read_data()
        # adc.read_status()
        # ch3_data = adc.read_data()
        # adc.read_status()
        # ch4_data = adc.read_data()
        # adc.read_status()
        # ch5_data = adc.read_data()
        # adc.read_status()
        # # ch2_data = adc.read_data()
        # adc.read_die_temp(ch0_data)
        # # adc.read_die_temp(ch1_data)
        # # adc.read_die_temp(ch2_data)
        # adc.test_conversion(ch1_data)
        # adc.test_conversion(ch2_data)
        # adc.test_conversion(ch3_data)
        # adc.test_conversion(ch4_data)
        # # adc.test_conversion(ch5_data)
        # adc.read_die_temp(ch5_data)
    
    adc.close()
    
if __name__ == "__main__":
    main()