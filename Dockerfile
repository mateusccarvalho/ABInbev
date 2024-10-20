FROM apache/airflow:2.7.1-python3.11

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev openjdk-11-jdk && \
    apt-get clean

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH" 

USER airflow

RUN pip install --upgrade apache-airflow-providers-openlineage>=1.8.0 && \
    pip install apache-airflow-providers-apache-spark && \
    #pip install apache-airflow-providers-papermill && \
    #pip install papermill && \
    pip install jupyter

EXPOSE 8888

WORKDIR /home/airflow/work

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
