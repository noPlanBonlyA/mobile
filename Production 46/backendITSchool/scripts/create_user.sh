#!/bin/bash

uv run python -m scripts.create_user --username ab --password 12 --role admin --first_name Pavel --surname Kozhinov --patronymic Sergeevich --email anthocyane@yandex.ru --phone_number +79642501607

uv run python -m scripts.create_user --username a --password 12 --role student --first_name Pavel --surname Kozhinov --patronymic Sergeevich --email pavel.seko4@gmail.com --phone_number +79642501606 --points 200

uv run python -m scripts.create_user --username abc --password 123 --role superadmin --first_name Eduard --surname Topalov --patronymic ZVZV --email ZVZV@yandex.ru --phone_number +79818515664

uv run python -m scripts.create_user --username adavvc --password 12 --role teacher --first_name Pavel --surname Kozhinov --patronymic Sergeevich --email p12113avel.seko6@gmail.com --phone_number +79648701406

uv run python -m scripts.create_user --password 1 --role superadmin --first_name a --surname a --patronymic c --email a@email.ru --birth_date 11.07.2000 --phone_number +79642501606
