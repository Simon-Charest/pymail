from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    argument_parser: ArgumentParser = ArgumentParser()
    argument_parser.add_argument("-s", "--save-configuration", action="store_true", help="save configuration")
    argument_parser.add_argument("-d", "--delete-messages", action="store_true", help="delete messages")
    argument_parser.add_argument("-m", "--max-count", type=int, help="maximum number of messages to process")
    argument_parser.add_argument("-g", "--get-messages", action="store_true", help="get messages")
    argument_parser.add_argument("-e", "--generate-graph", action="store_true", help="generate graph")
    argument_parser.add_argument("-r", "--generate-report", action="store_true", help="generate report")
    argument_parser.add_argument("-n", "--send-message", action="store_true", help="send message")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    arguments: Namespace = argument_parser.parse_args()

    return arguments
