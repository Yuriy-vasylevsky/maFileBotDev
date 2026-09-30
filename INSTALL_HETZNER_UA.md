# Встановлення бота на Hetzner

Файли бота вже мають бути завантажені на сервер в одну папку, наприклад `/root/opt`.

## 1. Підключіться до сервера

Відкрийте SSH-термінал у Termius і виконайте:

```bash
cd /root/opt
ls
```

У списку мають бути `compose.yaml`, `.env`, `Dockerfile` і папка `deploy`.

## 2. Встановіть Docker

```bash
sudo bash deploy/install-ubuntu.sh
```

## 3. Заповніть `.env`

```bash
nano .env
```

Перевірте насамперед:

- `BOT_TOKEN` — токен бота від BotFather;
- `ADMIN_ID` — Telegram ID адміністратора;
- `POSTGRES_PASSWORD` — пароль бази даних;
- такий самий пароль у рядку `DATABASE_URL`;
- `ENCRYPTION_KEY`, `MONO_TOKEN`, `SUPPORT_USERNAME` та `MANUAL_CARD`.

Зберегти файл у `nano`: **Ctrl+O**, **Enter**, потім **Ctrl+X**.

Захистіть файл із паролями:

```bash
chmod 600 .env
```

## 4. Запустіть бота

```bash
bash deploy/start.sh
```

Готово. Бот надалі автоматично запускатиметься після перезавантаження сервера.

## Перевірка

```bash
docker compose ps
docker compose logs --tail=100 app
```

У статусі контейнера `app` має бути `Up` або `healthy`. Вихід із перегляду логів: **Ctrl+C**.

## Після повторного завантаження нових файлів

```bash
cd /root/opt
docker compose up -d --build --force-recreate app
```
