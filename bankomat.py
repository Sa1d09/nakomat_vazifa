import psycopg2

conn = psycopg2.connect(
    dbname="bankomat",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

print("=== Bankomatga xush kelibsiz ===")

karta = input("Karta raqamingizni kiriting: ")
kod = input("Kodni kiriting: ")

cur.execute("SELECT id, balans FROM users WHERE karta=%s AND kod=%s", (karta, kod))
user = cur.fetchone()

if user:
    print("Kirish muvaffaqiyatli")
    while True:
        print("\n1. Balansni korish")
        print("2. Pul yechish")
        print("3. Chiqish")
        tanlov = input("Tanlang: ")

        if tanlov == "1":
            cur.execute("SELECT balans FROM users WHERE id=%s", (user[0],))
            balans = cur.fetchone()[0]
            print("Balansingiz:", balans, "som")

        elif tanlov == "2":
            miqdor = int(input("Qancha pul yechmoqchisiz? "))
            cur.execute("SELECT balans FROM users WHERE id=%s", (user[0],))
            balans = cur.fetchone()[0]

            if balans >= miqdor:
                yangi_balans = balans - miqdor
                cur.execute("UPDATE users SET balans=%s WHERE id=%s", (yangi_balans, user[0]))
                conn.commit()
                print("Pul yechildi Yangi balans:", yangi_balans, "som")
            else:
                print("Balansda yetarli mablag yoq")

        elif tanlov == "3":
            print("Bankomatdan foydalanganingiz uchun rahmat")
            break
        else:
            print("notogri tanlov")
else:
    print("Karta raqami yoki kod notogri")

cur.close()
conn.close()