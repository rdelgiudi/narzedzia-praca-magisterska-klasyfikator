##################################
# Program generujący plik annotations wymagany do wskazania datasetu
# Sposób użycia: umieść program w folderze test lub train, 
# wpisz ilość każdego z reprezentantów w folderze oraz uruchom
##################################

f = open("annotations.txt", "w")

for i in range(1, 101):
    f.write(f"grooming/{i:04d} 0 120 0\n")

for i in range(1, 101):
    f.write(f"idle/{i:04d} 0 120 1\n")

for i in range(1, 101):
    f.write(f"reeling/{i:04d} 0 120 2\n")