import json
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Response
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from pytz import utc

from mail import Mail
from schema import UserSchema
from logs import logger

STARTED = False


def consumer():
    global STARTED
    logger.info('started')
    if not STARTED:
        STARTED = True
        try:
            consumer = KafkaConsumer(
                'send_mail',
                bootstrap_servers=os.environ.get("BOOTSTRAP_SERVERS"),
            )
        except KafkaError as exc:
            logger.error(f"Kafka consumer - Exception during connecting to broker - {exc}")
            STARTED = False
            return Response(status=500)
        for message in consumer:
            record = json.loads(message.value)
            for item in record.get("items", []):
                data = UserSchema().dump(item)
                if data['mail'] and data['subject'] and data['text']:
                    result = mail_sender.send_mail(data)
                    time.sleep(1)
                    logger.error(result)
                    STARTED = False
                    return Response(status=200)
                else:
                    logger.error('Your mail-data is invalid!')
                    STARTED = False
                    return Response(status=400)
    STARTED = False


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
mail_sender = Mail()

if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    try:
        schedule = BackgroundScheduler(daemon=True, job_defaults={'max_instances': 6000}, timezone=utc)
        schedule.add_job(consumer, 'interval', seconds=os.environ.get("SCHEDULE_INTERVAL", 30))
        schedule.start()
    except Exception as er:
        logger.error(f"APScheduler_Error: {er}")


@app.route('/')
def main():
    return "Main"


@app.route('/mailing', methods=['POST'])
def mailing():
    request_data = request.get_json(force=True)
    err = UserSchema().validate(request_data)
    if err:
        logger.error("Mail-data:", err)
        return Response(err, status=400)
    else:
        result = mail_sender.send_mail(request_data)
        logger.info(f"Sending mail result: {result}")
        return Response(result, status=200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=os.environ.get('DEBUG', False), use_reloader=False)
