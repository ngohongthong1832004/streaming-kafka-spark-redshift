FROM bitnami/spark:latest

USER root
RUN install_packages curl

# Redshift JDBC driver
COPY redshift-jdbc42-2.1.0.32.jar /opt/bitnami/spark/jars/redshift-jdbc42.jar

# Kafka connectors
RUN curl -L -o /opt/bitnami/spark/jars/spark-sql-kafka.jar \
    https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar && \
    curl -L -o /opt/bitnami/spark/jars/kafka-clients.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.0/kafka-clients-3.5.0.jar && \
    curl -L -o /opt/bitnami/spark/jars/spark-token-provider-kafka.jar \
    https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar

USER 1001
