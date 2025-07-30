from faker import Faker
from datetime import datetime
import random
import csv
import matplotlib.pyplot as plt
import pandas as pd

fake = Faker()

# Sağlık konulu yorumlar
health_comments = [
    "Sağlıklı yaşamak çok önemli.",
    "Koronavirüsten korunmak için maske takmayı ihmal etmeyin.",
    "Her gün en az 30 dakika egzersiz yapmak sağlığımız için çok önemli.",
    "Grip aşısını yaptırmak, virüsün yayılmasını önlemek için önemlidir.",
    "Dengeli beslenmek ve yeterli su tüketmek vücudumuz için çok önemlidir.",
]

# 1. Önce veri setini oluştur
with open('health_comments.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Kullanıcı Adı', 'Yorum', 'Tarih/Saat', 'Beğeni Sayısı', 'Retweet Sayısı', 'Konum'])
    for i in range(500):
        comment = random.choice(health_comments)
        date_time = fake.date_time_between(start_date='-1y', end_date='now')
        likes = random.randint(0, 100)
        retweets = random.randint(0, 50)
        location = fake.city()
        writer.writerow([fake.user_name(), comment, date_time, likes, retweets, location])

# 2. Veri setini oku
data = pd.read_csv('health_comments.csv')

# 3. Saat bazında yorum sayısı histogramı
plt.figure(figsize=(10, 6))
plt.hist(data['Tarih/Saat'].str.split(' ').str[1].str.split(':').str[0].astype(int), bins=24, edgecolor='black')
plt.xlabel('Saat')
plt.ylabel('Yorum Sayısı')
plt.title('Saat Bazında Yorum Sayısı')
plt.xticks(range(0, 24))
plt.grid(True)
plt.show()

# 4. Gün bazında yorum sayısı pasta grafiği
day_counts = data['Tarih/Saat'].apply(lambda x: pd.Timestamp(x).day_name()).value_counts()
plt.figure(figsize=(10, 6))
plt.pie(day_counts, labels=day_counts.index, autopct='%1.1f%%')
plt.title('Gün Bazında Yorum Sayısı')
plt.show()

# 5. Beğeni ve retweet saçılma grafiği
plt.figure(figsize=(10, 6))
plt.scatter(data['Beğeni Sayısı'], data['Retweet Sayısı'], alpha=0.5)
plt.xlabel('Beğeni Sayısı')
plt.ylabel('Retweet Sayısı')
plt.title('Beğeni Sayısı ve Retweet Sayısı Arasındaki İlişki')
plt.grid(True)
plt.show()

# 6. Saat ve gün analizleri
hours = [0] * 24
days = [0] * 7

with open('health_comments.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Header'ı atla
    for row in reader:
        date_str = row[2]
        date_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        hour = date_time.hour
        day = date_time.weekday()
        hours[hour] += 1
        days[day] += 1

# 7. En çok yorum yapılan saat ve gün
max_hour = hours.index(max(hours))
print(f'En çok yorum yapılan saat: {max_hour}:00 - {(max_hour+1)%24}:00')

max_day = days.index(max(days))
day_names = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
print(f'En çok yorum yapılan gün: {day_names[max_day]}')
