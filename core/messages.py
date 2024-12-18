import json
import typing


class Messages:
    def __init__(self):
        self.__content = {}

    def load(self) -> None:
        with open("source/message and reply.json", "r") as json_file:
            self.__content = json.load(json_file)

    def save(self) -> None:
        with open("source/message and reply.json", "w") as file:
            file.write(json.dumps(self.__content))

    def set(self, message: str, data: dict):
        self.__content[message] = data

    def get(self, message: str):
        return self.__content[message]

    def delete(self, message: str) -> None:
        self.__content.pop(message)

    def clear(self) -> None:
        self.__content = {}

    def message_names(self) -> typing.List[str]:
        return list(self.__content.keys())

    def content(self):
        return self.__content

    def new_id(self) -> str:
        int_message_names = list(
            filter(lambda name: name.isnumeric(), self.message_names())
        )
        return str(int(int_message_names[-1]) + 1) if int_message_names else "1"


messages = Messages()
