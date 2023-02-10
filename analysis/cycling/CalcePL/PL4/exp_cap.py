def cap(cycle_no):
    A = 2.538
    b = 0.454
    NDC = 100.0 - A * (cycle_no/100)**b
    return NDC