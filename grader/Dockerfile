FROM ubuntu:16.04

# Install Java on your ubuntu image.
RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

# Install Python3.6
RUN apt-get update && \
        apt-get install -y software-properties-common vim && \
        add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update -y

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv && \
        apt-get install -y git

RUN \
  cd /usr/lib && \
  apt-get update && \
  apt-get install -y unzip zip && \
  apt-get install wget && \
  wget --quiet https://github.com/JetBrains/kotlin/releases/download/v1.3.11/kotlin-compiler-1.3.11.zip && \
  unzip kotlin-compiler-*.zip && \
  rm kotlin-compiler-*.zip && \
  rm kotlinc/bin/*.bat && \
  ln -s /usr/lib/kotlinc/bin/kotlinc /usr/bin/kotlinc

RUN mkdir /grader

COPY grader/execute_grader.py /grader/execute_grader.py
COPY src/test/hidden grader/src/test/hidden
COPY src/test/initial grader/src/test/initial
COPY grader/src/main/TestRunner.kt /grader/TestRunner.kt
COPY grader/junit-4.12.jar /grader/junit-4.12.jar
COPY grader/hamcrest-core-1.3.jar /grader/hamcrest-core-1.3.jar
COPY grader/gson-2.8.5.jar /grader/gson-2.8.5.jar


RUN chmod a+rwx -R /grader/

ENTRYPOINT ["python3.6", "./grader/execute_grader.py"]