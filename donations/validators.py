import re
from django.core.exceptions import ValidationError


class FNGCCValidator:
    message = 'Invalid credit card.'
    code = 'invalid'

    def __call__(self, value):
        """
        Validate that the input contains (or does *not* contain, if
        inverse_match is True) a match for the regular expression.
        """
        valid_input = self.creditCard(ccnumber=value)['valid']
        if not valid_input:
            raise ValidationError(self.message, code=self.code)

    def creditCard(self, ccnumber, cardtype='', allowTest=False):
        # Check for test cc number
        if(allowTest is False and ccnumber == '4111111111111111'):
            return False

        ccnumber = re.sub("[^0-9]", "", ccnumber)

        creditcard = {
            'visa': "^4[0-9]{12}(?:[0-9]{3})?$",
            'mastercard': "^(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))$",
            'discover': "^6011-?\d{4}-?\d{4}-?\d{4}",
            'amex': "^3[47][0-9]{13}$",
            'diners': "^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
            'bankcard': "^5610-?\d{4}-?\d{4}-?\d{4}",
            'jcb': "^(?:2131|1800|35\d{3})\d{11}$",
            'enroute': "^[2014|2149]\d{11}",
            'switch': "^[4903|4911|4936|5641|6333|6759|6334|6767]\d{12}"
        }

        if not cardtype:
            match = False
            for key, pattern in creditcard.items():
                if re.search(pattern, ccnumber):
                    match = True
                    cardtype = key
                    break

            if not match:
                return False

        elif not re.search(creditcard[(cardtype.strip()).lower()], ccnumber):
            return False

        return {
            'valid': self.luhnCheck(ccnumber),
            'ccnum': ccnumber,
            'type': cardtype
        }

    def luhnCheck(self, ccnum):
        checksum = 0
        for i in range(2-(len(ccnum) % 2), len(ccnum)+1, 2):
            checksum += int(ccnum[i-1])

        # Analyze odd digits in even length strings or even digits in odd length strings.
        for i in range((len(ccnum) % 2) + 1, len(ccnum), 2):
            digit = int(ccnum[i-1]) * 2
            if digit < 10:
                checksum += digit
            else:
                checksum += (digit-9)

        if checksum % 10 == 0:
            return True
        else:
            return False
