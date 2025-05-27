import argparse
from logging import basicConfig, StreamHandler, DEBUG, CRITICAL, ERROR, WARNING, INFO

from hs_temp_sensor import ad7124

def main() -> None:
    parser = argparse.ArgumentParser(description="HISPEC 4-wire Temperature Sensor Test Software")
    parser.add_argument("-v", "--verbose", dest="verbosity", action="count", default=0,
                        help="Verbosity (between 1-4 occurrences with more leading to more verbose logging)" \
                        "CRITICAL=0, ERROR=1, WARNING=2, INFO=3, DEBUG=4")
    
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
    adc.initialize()
    adc.read_id()
    adc.read_adc_config()
    adc.read_channel_config()
    adc.read_data()
    adc.configure()
    adc.read_adc_config()
    adc.read_channel_config()
    data = adc.read_data()
    adc.read_die_temp(data)
    
    
    
    # adc.read_die_temp()
    adc.close()
    
if __name__ == "__main__":
    main()