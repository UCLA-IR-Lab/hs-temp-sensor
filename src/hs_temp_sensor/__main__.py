from hs_temp_sensor import ad7124

def main() -> None:
    adc = ad7124.AD7124()
    adc.connect()
    adc.initialize()
    adc.read_id()
    adc.read_adc_config()
    adc.set_adc_config()
    adc.read_adc_config()
    # adc.read_die_temp()
    adc.close()
    
if __name__ == "__main__":
    main()