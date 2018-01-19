docker build -t hazel/pylons \
       --build-arg PIP_PKG_IDX_ARGS="${PIP_PKG_IDX_ARGS}" \
       .
