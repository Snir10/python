
binary_word = "1000110011010101111000000001"
dyn_counter = 0
maxcounter = 0


for i in binary_word:
    if i == '1':
        if maxcounter <= dyn_counter:
            maxcounter = dyn_counter

        dyn_counter = 0
    else:
        dyn_counter = dyn_counter + 1


print(maxcounter)