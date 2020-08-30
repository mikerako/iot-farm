import csv
import random

def main():
    with open('random.csv', 'w', newline='') as csvfile:
        random.seed()

        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['timestamp', 'temperature', 'humidity', 'co2', 'pressure'])
        
        for i in range(10000):
            temp = random.randrange(-40, 85) + random.random()
            humidity = random.randrange(0, 100) + random.random()
            co2 = random.randrange(0, 1187) + random.random()
            pressure = random.randrange(30000, 110000) + random.random()

            writer.writerow([i, temp, humidity, co2, pressure])


if __name__ == "__main__":
    main()
    print('done')
