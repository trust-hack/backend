## TRUST HACK BACKEND

### Установка
```bash
cat << EOF > .env-dc
MONGO_USER=<USER>
MONGO_PASS=<PASS>
EOF
docker-compose --env-file .env-dc up -d
```
