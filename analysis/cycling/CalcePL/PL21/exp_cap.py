def cap(cycle_no):
    A = 3.708
    b = 0.452
    NDC = 100.0 - A * (cycle_no/100)**b
    return NDC