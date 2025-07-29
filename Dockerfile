FROM alpine:3.20
RUN apk update
RUN apk add python3
RUN apk add py3-pip
WORKDIR /guestslist
COPY requirements.txt .
COPY guestlist-server.py .
RUN python3 -m venv guestlistenv
ENV PATH="/guestslist/guestlistenv/bin:$PATH"
RUN pip install -r requirements.txt
CMD ["python3", "guestlist-server.py"]


