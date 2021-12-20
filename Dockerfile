FROM python:3.8
COPY proxy_service /app
EXPOSE 5005
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["./run.sh"]
