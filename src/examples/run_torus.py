import subprocess
import re
import csv
import matplotlib.pyplot as plt

config = "torus88"

rates = [
    0.001,
    0.002,
    0.003,
    0.004,
    0.005,
    0.006,
    0.0065,
    0.0068,
    0.0070,
    0.0072
]

results = []

with open(config) as f:
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
        r"Packet latency average = ([\d.]+)",
        output
    )

    if matches:
        latency = float(matches[-1])
        results.append((rate, latency))
        print(f"Injection Rate: {rate:.4f}  Latency: {latency}")

with open(config, "w") as f:
    f.write(original)

with open("torus_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Injection Rate", "Packet Latency"])
    writer.writerows(results)

x = [a for a, b in results]
y = [b for a, b in results]

plt.plot(x, y, marker="o")
plt.xlabel("Injection Rate")
plt.ylabel("Average Packet Latency (cycles)")
plt.title("8x8 Torus - Latency vs Offered Load")
plt.grid(True)
plt.savefig("torus_latency.png", dpi=300)
