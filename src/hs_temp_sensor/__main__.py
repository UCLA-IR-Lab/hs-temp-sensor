from logging import basicConfig, StreamHandler, DEBUG

from hs_temp_sensor import ad7124

def main() -> None:
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
    basicConfig(
        level=DEBUG,
        format='%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s'
    )

    main()