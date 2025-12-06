from utils import File as UtilsFile


class File(UtilsFile):
    def has_changed(self, content):
        if not self.exists:
            return True
        existing_content = self.read()
        return existing_content != content

    def write_if_changed(self, content):
        if self.has_changed(content):
            self.write(content)
            return True
        return False
