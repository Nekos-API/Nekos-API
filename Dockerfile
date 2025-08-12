FROM rust:latest

WORKDIR /app
COPY . .

RUN cargo build --release

ENTRYPOINT [ "cargo" ]
CMD [ "run", "--release" ]
EXPOSE 3000
