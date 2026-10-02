import matplotlib.pyplot as plt

tries = [i for i in range(1, 12)]
results = [0.01, 0.14, 0.20, 0.18, 0.12, 0.20, 0.19, 0.18, 0.18, 0.16, 0.20]

fig, ax = plt.subplots()
ax.plot(tries, results, linewidth=2, color="red")
ax.scatter(tries, results, color="red")

ax.set_title("Training v1", fontsize=24)
ax.set_xlabel("Evaluation Points", fontsize=16)
ax.set_ylabel("SCORE", fontsize=16)
ax.tick_params(labelsize=16)

plt.xticks(tries) # x de 1 à 11
plt.ylim(0, 1) # y = de 0 à 1

plt.show()
#plt.savefig("Training_v1")
