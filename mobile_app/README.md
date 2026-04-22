# mobile_app

React Native (Expo) обертка для сайта `front_it_school` через `WebView`.

## 1. Быстрый старт

```bash
cd mobile_app
cp .env.example .env
npm install
npm start
```

Потом открой:
- `a` для Android emulator
- `i` для iOS simulator
- Expo Go на телефоне (скан QR)

## 2. URL сайта для обертки

В `.env` используются переменные:

```env
EXPO_PUBLIC_WEB_URL_ANDROID=http://10.0.2.2:3000
EXPO_PUBLIC_WEB_URL_IOS=http://localhost:3000
```

Рекомендации:
- Android emulator: `http://10.0.2.2:3000`
- iOS simulator: `http://localhost:3000`
- Физический телефон: `http://<LAN_IP_ТВОЕГО_ПК>:3000`

Можно также оставить общую переменную `EXPO_PUBLIC_WEB_URL` — она будет fallback для обеих платформ.

## 3. Что уже реализовано

- Загрузка сайта в `WebView`
- Экран загрузки и экран ошибки с кнопкой перезагрузки
- Back-кнопка Android (идет назад по истории WebView)
- Ограничение на переходы: сторонние ссылки открываются в системном браузере
- Базовые настройки cookie/session для авторизации

## 4. Важно для локального теста с телефоном

Если тестируешь на физическом телефоне, `localhost` указывает на сам телефон, а не на твой компьютер.  
Нужен LAN IP компьютера и открытые порты.

Минимум:
1. Поднять фронт на `0.0.0.0:3000`.
2. Поднять бек так, чтобы он был доступен с телефона.
3. Если фронт ходит в API через абсолютный `localhost`, замени на LAN IP или настрой same-origin через reverse proxy (`/api`).

Примечание:
- В `app.json` включен `android.usesCleartextTraffic=true` для локальной разработки с `http`.
- Для продакшна лучше использовать `https` и убрать `http`-доступ.
