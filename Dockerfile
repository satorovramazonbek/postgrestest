# Asos sifatida Python 3.12 ning yengil (slim) Linux image'i olinadi
FROM python:3.12-slim

# Konteyner ichidagi ishchi papka (keyingi buyruqlar shu papkada bajariladi)
WORKDIR /app

# Avval faqat requirements.txt nusxalanadi - kutubxonalar o'zgarmasa Docker bu qadamni keshdan oladi
COPY requirements.txt .

# Kutubxonalarni o'rnatish; --no-cache-dir image hajmini kichik qiladi
RUN pip install --no-cache-dir -r requirements.txt

# Dastur kodi nusxalanadi
COPY aaa.py .

# Bazaga ulanish sozlamalari (docker run -e ... bilan almashtirish mumkin).
# host.docker.internal - konteyner ichidan sizning kompyuteringizga (localhost'ga) murojaat qilish manzili
ENV DB_HOST=host.docker.internal \
    DB_PORT=5432 \
    DB_NAME=postgrestest \
    DB_USER=postgres

# Konteyner ishga tushganda bajariladigan buyruq
CMD ["python", "aaa.py"]
