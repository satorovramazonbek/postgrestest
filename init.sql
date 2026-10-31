-- Test bazasi uchun talabalar jadvali (CI shu fayldan jadval yaratadi)
DROP TABLE IF EXISTS talabalar;

CREATE TABLE talabalar (
    id integer PRIMARY KEY,
    ism varchar(50) NOT NULL,
    familiya varchar(50) NOT NULL,
    yosh integer,
    shahar varchar(50),
    kurs varchar(50),
    ball integer,
    tolov integer
);

INSERT INTO talabalar VALUES
    (1, 'Aziz', 'Karimov', 17, 'Toshkent', 'Python', 85, 550000),
    (2, 'Dilnoza', 'Rahimova', 19, 'Samarqand', 'Web dizayn', 92, 450000),
    (3, 'Sardor', 'Aliyev', 16, 'Toshkent', 'Kompyuter savodxonligi', 74, 300000);
