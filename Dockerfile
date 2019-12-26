FROM rust:alpine

WORKDIR /mrrobot
COPY . .

RUN cargo build

ENTRYPOINT ["cargo","run","--"]