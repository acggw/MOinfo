import subprocess
import time

# List your consumer scripts
services = [
    "Scripts/clock.py",
    "Scripts/missouri_house_retreiver.py",
    "Scripts/missouri_senate_retreiver.py",
    "Scripts/emails.py",
    "Scripts/notifications.py",
    "Scripts/process_bills.py",
    "Scripts/website_updates.py"
]

processes = []

def start_all():
    print("Starting Kafka services...")

    for service in services:
        print(f"Launching {service}...")
        p = subprocess.Popen(["python", service])#,
        #                    stdout=subprocess.PIPE,   # capture standard output
        #                    stderr=subprocess.PIPE,   # capture error output
        #                    text=True
        #)
        processes.append(p)

    print(f"{len(processes)} services started.\n")

def monitor_processes():
    print("Monitoring processes (Ctrl+C to exit)...")

    try:
        while True:
            for i, p in enumerate(processes):
                if p.poll() is not None:   # process crashed
                    processes[i] = subprocess.Popen(["python", services[i]])
                else:
                    pass
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping consumers...")
        for p in processes:
            p.terminate()
        print("All consumers stopped.")

if __name__ == "__main__":
    start_all()
    monitor_processes()
    



