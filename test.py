from PPM.PPM import My_PPM
import time

if __name__ == "__main__":
    ppm = My_PPM()
    time.sleep(3)
    vals = [2000, 2000, 2000, 2000, 1000, 1000, 1000, 1000]
    ppm.update_ppm_channels(vals)
    
