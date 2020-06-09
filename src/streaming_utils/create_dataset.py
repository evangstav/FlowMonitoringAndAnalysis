import client
import csv
import random

labels = []
msgs = []
for i in range(1000):
    c = client.NoisyClient(port=1233, noise=random.random())
    m = c.get_message()
    n = c.get_noise()
    labels.append(n)
    msgs.append(m)

with open("raw.csv", "w", newline="") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(msgs)

with open("labels.csv", "w", newline="") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(labels)
