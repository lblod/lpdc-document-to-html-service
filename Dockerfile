FROM semtech/mu-python-template:feature-no-more-meinheld
LABEL maintainer="loketlokaalbestuur@vlaanderen.be"


ENV DOCLING_ARTIFACTS_PATH=/opt/docling/models

RUN mkdir -p "$DOCLING_ARTIFACTS_PATH" \
    && docling-tools models download \
        --output-dir "$DOCLING_ARTIFACTS_PATH"

