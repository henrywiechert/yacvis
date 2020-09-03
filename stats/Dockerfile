FROM python:3-onbuild

# install cron and add a job that fetches the data regularly
RUN apt-get update
RUN apt-get install -y cron
COPY stats.cron /etc/cron.d/stats.cron
RUN chmod 0644 /etc/cron.d/stats.cron
RUN crontab /etc/cron.d/stats.cron

# git status/revision into ENV variables
ARG GIT_COMMIT=unspecified
ARG WS_STATUS=unspecified
LABEL git_commit=$GIT_COMMIT
LABEL git_dirty=$WS_STATUS
ENV GIT_SHA=${GIT_COMMIT}
ENV GIT_STATUS=${WS_STATUS}

# exposed port
EXPOSE 8050

CMD ["bash", "./run.bash"]
