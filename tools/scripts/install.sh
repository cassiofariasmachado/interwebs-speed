#!/bin/bash

source .env

echo '✅ install helm'
helm install interwebs-speed tools/helm \
    --set-string configs.CSV_FILES_PATH="${CSV_FILES_PATH}" \
    --set-string configs.INTERNET_SPEED="${INTERNET_SPEED}" \
    --set-string configs.EXPECTED_DOWNLOAD="${EXPECTED_DOWNLOAD}" \
    --set-string configs.EXPECTED_UPLOAD="${EXPECTED_UPLOAD}" \
    --set-string configs.SMTP_HOST="${SMTP_HOST}" \
    --set-string configs.SMTP_PORT="${SMTP_PORT}" \
    --set-string configs.ALERT_SENDER_MAIL="${ALERT_SENDER_MAIL}" \
    --set-string configs.ALERT_RECEIVER_MAIL="${ALERT_RECEIVER_MAIL}" \
    --set-string secrets.SMTP_USERNAME="${SMTP_USERNAME}" \
    --set-string secrets.SMTP_PASSWORD="${SMTP_PASSWORD}"
