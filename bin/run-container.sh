docker run -it \
    -e SESSION_KEY=$(pwgen 32 1) \
    -e JWT_PUBLIC_KEY=$(pwgen 32 1) \
    -e JWT_PRIVATE_KEY=$(pwgen 32 1) \
    -e DATABASE_URL=${DATABASE_URL} \
    -e SMTP_HOST=${SMTP_HOST} \
    -e SMTP_PORT=${SMTP_PORT} \
    -e SMPT_USERNAME=${SMTP_USERNAME} \
    -e SMPT_PASSWORD=${SMTP_PASSWORD} \
    -p 6543:6543 \
    hazel/pylons
