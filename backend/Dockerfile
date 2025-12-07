FROM python:3.9-alpine
WORKDIR /backend
COPY requirements.txt /backend
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
COPY . .

ENV FLASK_APP main.py
ENV FLASK_ENV production
ENV FLASK_RUN_PORT 31337
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 31337

CMD ["flask", "run"]