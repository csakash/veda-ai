import pysrt, os

for filename in os.listdir("./Ai Subs"):
    subs = pysrt.open("./Ai Subs/"+filename, encoding='iso-8859-1')

    with open("./subs/"+filename[:len(filename)-4]+".txt", "w") as f:
        for sub in subs:
            f.write(sub.text)