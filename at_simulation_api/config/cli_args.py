import argparse
import os


def parse_db_args(subparsers: argparse._SubParsersAction):
    db_parser = subparsers.add_parser("db", help="Database configuration.")
    db_parser.add_argument("--DB_HOST", type=str, help="Database host.")
    db_parser.add_argument("--DB_PORT", type=int, help="Database port.")
    db_parser.add_argument("--DB_NAME", type=str, help="Database name.")
    db_parser.add_argument("--DB_USER", type=str, help="Database user.")
    db_parser.add_argument("--DB_PASS", type=str, help="Database password.")
    return db_parser


def parse_minio_args(subparsers: argparse._SubParsersAction):
    minio_parser = subparsers.add_parser("minio", help="Minio configuration.")
    minio_parser.add_argument("--MINIO_HOST", type=str, help="Minio host.")
    minio_parser.add_argument("--MINIO_ACCESS_KEY", type=str, help="Minio access key.")
    minio_parser.add_argument("--MINIO_SECRET_KEY", type=str, help="Minio secret key.")
    minio_parser.add_argument(
        "--MINIO_SECURE", type=bool, help="Use secure connection."
    )
    minio_parser.add_argument(
        "--MINIO_BUCKET_NAME", type=str, help="Minio bucket name."
    )
    minio_parser.add_argument("--MINIO_API_PORT", type=int, help="Minio API port.")
    minio_parser.add_argument(
        "--MINIO_CONSOLE_PORT", type=int, help="Minio console port."
    )
    return minio_parser


def parse_rabbitmq_args(subparsers: argparse._SubParsersAction):
    rabbitmq_parser = subparsers.add_parser("rabbitmq", help="RabbitMQ configuration.")
    rabbitmq_parser.add_argument("--RABBITMQ_HOST", type=str, help="RabbitMQ host.")
    rabbitmq_parser.add_argument("--RABBITMQ_PORT", type=int, help="RabbitMQ port.")
    rabbitmq_parser.add_argument("--RABBITMQ_LOGIN", type=str, help="RabbitMQ login.")
    rabbitmq_parser.add_argument(
        "--RABBITMQ_PASSWORD", type=str, help="RabbitMQ password."
    )
    rabbitmq_parser.add_argument(
        "--RABBITMQ_VHOST", type=str, help="RabbitMQ virtualhost."
    )
    rabbitmq_parser.add_argument(
        "--RABBITMQ_SSL", type=bool, help="Use SSL for RabbitMQ."
    )
    return rabbitmq_parser


def parse_server_args(subparsers: argparse._SubParsersAction):
    server_parser = subparsers.add_parser("server", help="Server configuration.")
    server_parser.add_argument("--SERVER_PORT", type=int, help="Server port.")
    return server_parser


def parse_args():
    parser = argparse.ArgumentParser(description="Main application configuration.")
    subparsers = parser.add_subparsers(dest="command")

    parse_db_args(subparsers)
    parse_minio_args(subparsers)
    parse_rabbitmq_args(subparsers)
    parse_server_args(subparsers)
    args = parser.parse_args()
    
    for key, value in vars(args).items():
        if value is not None:
            os.environ[key.upper()] = str(value)
