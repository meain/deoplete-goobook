import subprocess
from subprocess import CalledProcessError

from .base import Base


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.rank = 100
        self.name = "goobooks"
        self.description = "name and emails from your google accounts"
        self.mark = "[gc]"
        self.filetypes = []

    def on_init(self, context):
        self.executable = context["vars"].get(
            "deoplete#sources#goobook#executable", ["goobook"]
        )

    def gather_candidates(self, context):
        try:
            contacts = subprocess.check_output(
                self.executable + ["query", "@"], universal_newlines=True
            ).split("\n")[1:-1]
        except CalledProcessError:
            return []
        results = []
        for contact in contacts:
            email, name, *_ = contact.split("\t")
            results += [
                {"word": email, "kind": "email"},
                {"word": name, "kind": "name"},
            ]
        return results
