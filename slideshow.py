import julia
import time

ct = time.localtime()
julia.julia(julia.pickTimeInterest(), (ct.tm_hour % 6 + 2), pickColor=julia.timeBased, height=500, width=500).show()
