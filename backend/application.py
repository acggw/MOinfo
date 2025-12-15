import subprocess
import time

# List your consumer scripts
services = [
    "backend/clock.py",
    "retreivers/missouri_house_retreiver.py",
    #"retreivers/missouri_senate_retreiver.py",
    #"notifications/emails.py",
    "notifications/notifications.py",
    "notifications/emails.py",
    #"Scripts/website_updates.py",
]

def start_all():
    processes = []
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

    return processes

def monitor_processes(processes):
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
    processes = start_all()
    monitor_processes(processes)
    



