import re
from lib.validators.qcommon_validator import QCommonValidator


class QDsNameValidator(QCommonValidator):

    def __init__(self, name_type=None, parent=None):
        super(QDsNameValidator, self).__init__(parent)

        self.name_type = name_type
        if self.name_type is None:
            self.regX_expression = re.compile('^([a-zA-Z@#$])([a-zA-Z@#$0-9]{0,7})$')

        else:
            self.regX_expression = re.compile('^([a-zA-Z@#$])([a-zA-Z@#$0-9]{0,6})$')

    def validate(self, text_input, pos):
        matches = self.regX_expression.findall(text_input)
        if matches and len("".join(matches[0])) == len(text_input):
            if len(text_input) == 0:
                return self.return_state(self.STATE_INTERMEDIATE, text_input, pos)

            else:
                return self.return_state(self.STATE_ACCEPTABLE, text_input, pos)

        else:
            if len(text_input) == 0:
                return self.return_state(self.STATE_INTERMEDIATE, text_input, pos)

            else:
                return self.return_state(self.STATE_INVALID, text_input, pos)
