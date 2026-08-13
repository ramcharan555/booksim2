import subprocess
import re
import csv
import matplotlib.pyplot as plt

config = "mesh88_lat"

rates = [
    0.001,
    0.002,
    0.003,
    0.004,
0.0046,
 0.005,
0.0057,
    0.006,
    0.0065,
    0.0070
]

results = []

with open(config, "r") as f:
    original = f.read()

for rate in rates:
    updated = re.sub(
        r"injection_rate\s*=\s*[\d.]+;",
        f"injection_rate = {rate};",
        original
    )

    with open(config, "w") as f:
        f.write(updated)

    output = subprocess.run(
        ["../booksim", config],
        capture_output=True,
        text=True
    ).stdout

    matches = re.findall(
        r"Packet latency average = ([\d.]+) \(1 samples\)",
        output
    )

    if matches:
        latency = float(matches[-1])
        results.append((rate, latency))
        print(f"Injection Rate: {rate:.3f}  Latency: {latency}")

with open(config, "w") as f:
    f.write(original)

with open("mesh_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Injection Rate", "Packet Latency"])
    writer.writerows(results)

x = [r[0] for r in results]
y = [r[1] for r in results]

plt.plot(x, y, marker="o")
plt.xlabel("Injection Rate")
plt.ylabel("Average Packet Latency (cycles)")
plt.title("8x8 Mesh - Latency vs Offered Load")
plt.grid(True)
plt.savefig("mesh_latency.png", dpi=300)
plt.show()
