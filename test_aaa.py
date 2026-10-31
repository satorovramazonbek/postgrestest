import builtins
from pathlib import Path

import pytest

import aaa

INIT_SQL = Path(__file__).with_name("init.sql").read_text()


@pytest.fixture
def conn():
    conn = aaa.connect()
    with conn.cursor() as cur:
        cur.execute(INIT_SQL)
    conn.commit()
    yield conn
    conn.close()


def javoblar(monkeypatch, *qiymatlar):
    """input() o'rniga tayyor javoblarni beradi"""
    it = iter(qiymatlar)
    monkeypatch.setattr(builtins, "input", lambda _="": next(it))


def bitta(conn, sql, params=()):
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def test_korish(conn, capsys):
    aaa.talabalarni_korish(conn)
    chiqish = capsys.readouterr().out
    assert "Aziz" in chiqish
    assert "Jami: 3 ta talaba" in chiqish


def test_qoshish(conn, monkeypatch):
    javoblar(monkeypatch, "4", "Madina", "Yusupova", "18", "Buxoro", "Python", "67", "550000")
    aaa.talaba_qoshish(conn)
    assert bitta(conn, "SELECT ism, ball FROM talabalar WHERE id = 4") == ("Madina", 67)


def test_ozgartirish(conn, monkeypatch):
    javoblar(monkeypatch, "1", "ball", "90")
    aaa.talabani_ozgartirish(conn)
    assert bitta(conn, "SELECT ball FROM talabalar WHERE id = 1") == (90,)


def test_notogri_ustun_ozgarmaydi(conn, monkeypatch, capsys):
    javoblar(monkeypatch, "1", "id; DROP TABLE talabalar", "0")
    aaa.talabani_ozgartirish(conn)
    assert "Bunday ustun yo'q" in capsys.readouterr().out
    assert bitta(conn, "SELECT count(*) FROM talabalar") == (3,)


def test_ochirish(conn, monkeypatch):
    javoblar(monkeypatch, "2")
    aaa.talabani_ochirish(conn)
    assert bitta(conn, "SELECT count(*) FROM talabalar") == (2,)
