import numpy
import math

def Huang(data):
    threshold=-1;
    first_bin=  0
    for ih in range(254):
        if data[ih] != 0:
            first_bin = ih
            break
    last_bin=254;
    for ih in range(254,-1,-1):
        if data[ih] != 0:
            last_bin = ih
            break
    term = 1.0 / (last_bin - first_bin)
    mu_0 = numpy.zeros(shape=(254,1))
    num_pix = 0.0
    sum_pix = 0.0
    for ih in range(first_bin,254):
        sum_pix = sum_pix + (ih * data[ih])
        num_pix = num_pix + data[ih]
        mu_0[ih] = sum_pix / num_pix 
    min_ent = float("inf")
    for it in range(254): 
        ent = 0.0
        for ih in range(it):
            mu_x = 1.0 / ( 1.0 + term * math.fabs( ih - mu_0[it]))
            if ( not ((mu_x  < 1e-06 ) or (mu_x > 0.999999))):
                ent = ent + data[ih] * (-mu_x * math.log(mu_x) - (1.0 - mu_x) * math.log(1.0 - mu_x) ) 
        if (ent < min_ent):
            min_ent = ent
            threshold = it
    return threshold