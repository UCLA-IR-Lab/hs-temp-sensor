from . import ad7124

def main() -> None:
    adc = ad7124.AD7124()
    adc.connect()
    adc.read_id()
    adc.close()
    
if __name__ == "__main__":
    main()