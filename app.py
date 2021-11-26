from flask import Flask, render_template, url_for, request, Response
from Schema import UserSchema
from mail import Mail
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route('/')
def main():

    return '@Hello Flask_mailing@'


@app.route('/mailing', methods=['POST'])
def mailing():
    request_data = request.get_json(force=True)
    err = UserSchema().validate(request_data)
    if err:
        return Response(err, status=400)
    else:
        mail = Mail(request_data)
        result = mail.send_mail()
        return Response(result, status=200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
