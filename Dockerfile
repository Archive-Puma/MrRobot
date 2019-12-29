# Base image
FROM rust:alpine
# Metadata
MAINTAINER Kike Fontán (@CosasDePuma) <kikefontanlorenzo@gmail.com>

# Arguments
ARG target=release

# Source code
WORKDIR /mrrobot
COPY . .
# Build
RUN cargo build --"$target"

# Run
ENTRYPOINT ["cargo","run","--$target","--"]