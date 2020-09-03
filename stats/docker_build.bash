#!/bin/bash

if [[ $(git diff HEAD --stat) != '' ]]; then
  WORKSPACE_STATUS='dirty'
else
  WORKSPACE_STATUS='clean'
fi

docker build --build-arg GIT_COMMIT=$(git rev-parse HEAD) --build-arg WS_STATUS=$WORKSPACE_STATUS -t dockerhenry/covid-stats .
