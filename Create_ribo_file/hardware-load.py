import psutil
import main

def get_process_info():
    pid = psutil.Process()
    cpu_percent = psutil.cpu_percent()
    memory_info = pid.memory_info()
    ram_usage = memory_info.rss / (1024 * 1024)
    return cpu_percent, ram_usage

if __name__ == '__main__':
    cpu_before, ram_before = get_process_info()
    main.main()
    cpu_after, ram_after = get_process_info()

    cpu_count = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq().max
    total_memory = psutil.virtual_memory().total / (1024 * 1024 * 1024)

    print(f"CPU usage: {cpu_after - cpu_before:.2f}%")
    print(f"RAM usage: {ram_after - ram_before:.2f}MB")
    print('-' * 30)
    print(f"CPU Specs: {cpu_count} x {cpu_freq:.2f} GHz")
    print(f"RAM Specs: {total_memory:.2f} GB")