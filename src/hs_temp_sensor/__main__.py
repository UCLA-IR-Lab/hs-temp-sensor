from .ad7124 import AD7124

def main() -> None:
    adc = AD7124()
    adc.connect()
    adc.read_id()
    adc.close()
    
if __name__ == "__main__":
    main()