import os
from getpass import getpass

import psycopg2

# ====== Bazaga ulanish sozlamalari ======
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5432)),
    "dbname": os.environ.get("DB_NAME", "postgrestest"),
    "user": os.environ.get("DB_USER", "postgres"),
    # parol kodda saqlanmaydi: DB_PASSWORD o'zgaruvchisidan olinadi yoki so'raladi
    "password": os.environ.get("DB_PASSWORD") or getpass("Baza paroli: "),
}

USTUNLAR = ["ism", "familiya", "yosh", "shahar", "kurs", "ball", "tolov"]


def connect():
    return psycopg2.connect(**DB_CONFIG)


def talabalarni_korish(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM talabalar ORDER BY id")
        rows = cur.fetchall()
    print(f"\n{'id':>3} | {'ism':<10} | {'familiya':<12} | {'yosh':>4} | {'shahar':<10} | {'kurs':<23} | {'ball':>4} | {'tolov':>7}")
    print("-" * 95)
    for r in rows:
        print(f"{r[0]:>3} | {r[1]:<10} | {r[2]:<12} | {str(r[3]):>4} | {str(r[4]):<10} | {str(r[5]):<23} | {str(r[6]):>4} | {str(r[7]):>7}")
    print(f"Jami: {len(rows)} ta talaba")


def talaba_qoshish(conn):
    talaba_id = int(input("id: "))
    ism = input("ism: ")
    familiya = input("familiya: ")
    yosh = int(input("yosh: "))
    shahar = input("shahar: ")
    kurs = input("kurs: ")
    ball = int(input("ball: "))
    tolov = int(input("tolov: "))
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO talabalar (id, ism, familiya, yosh, shahar, kurs, ball, tolov) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (talaba_id, ism, familiya, yosh, shahar, kurs, ball, tolov),
        )
    conn.commit()
    print("Talaba qo'shildi")


def talabani_ozgartirish(conn):
    talaba_id = int(input("Qaysi talabani o'zgartiramiz (id): "))
    print("Ustunlar:", ", ".join(USTUNLAR))
    ustun = input("Qaysi ustun: ")
    if ustun not in USTUNLAR:
        print("Bunday ustun yo'q")
        return
    yangi = input("Yangi qiymat: ")
    with conn.cursor() as cur:
        # ustun nomi faqat USTUNLAR ro'yxatidan olinadi, shuning uchun xavfsiz
        cur.execute(f"UPDATE talabalar SET {ustun} = %s WHERE id = %s", (yangi, talaba_id))
        print(f"{cur.rowcount} ta qator o'zgartirildi")
    conn.commit()


def talabani_ochirish(conn):
    talaba_id = int(input("Qaysi talabani o'chiramiz (id): "))
    with conn.cursor() as cur:
        cur.execute("DELETE FROM talabalar WHERE id = %s", (talaba_id,))
        print(f"{cur.rowcount} ta qator o'chirildi")
    conn.commit()


def main():
    conn = connect()
    print("postgrestest bazasiga ulandi")
    try:
        while True:
            print("\n1 - talabalarni ko'rish")
            print("2 - talaba qo'shish")
            print("3 - talabani o'zgartirish")
            print("4 - talabani o'chirish")
            print("0 - chiqish")
            tanlov = input("Tanlang: ")
            try:
                if tanlov == "1":
                    talabalarni_korish(conn)
                elif tanlov == "2":
                    talaba_qoshish(conn)
                elif tanlov == "3":
                    talabani_ozgartirish(conn)
                elif tanlov == "4":
                    talabani_ochirish(conn)
                elif tanlov == "0":
                    break
                else:
                    print("Noto'g'ri tanlov")
            except (psycopg2.Error, ValueError) as e:
                conn.rollback()
                print("Xato:", e)
    finally:
        conn.close()
        print("Ulanish yopildi")


if __name__ == "__main__":
    main()
