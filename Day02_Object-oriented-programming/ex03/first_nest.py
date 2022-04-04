#!/usr/local/bin/python3

from multiprocessing.sharedctypes import Value
import sys
import os

######################
#      CLASSES       #
######################

class Research:
    """Class with research utils above the provided file
    """
    def __init__(self, filename: str) -> None:
        # filename
        self.filename = filename

        # csv file format
        self.separator = ','
        self.header_fields_number = 2
        self.correct_values = [('0', '1'),
                               ('1', '0')]

    def __is_correct_format(self, csv_data: list, has_header: bool) -> bool:
        # empty or header-only
        if len(csv_data) <= 1:
            return True

        # check header
        if has_header:
            header_fields = csv_data[0].split(self.separator)
            if len(header_fields) != self.header_fields_number: # correct number of fields
                return False

            for value in header_fields:                         # all non-empty
                if len(value) == 0:
                    return False

        # check other lines
        for index in range(1, len(csv_data)):
            if len(csv_data[index]) <= 1:   # empty lines
                continue

            values = csv_data[index].split(self.separator)
            if len(values) != self.header_fields_number:    # incorect number of fields
                return False

            value_tuple = (*values[:-1], values[-1].replace('\n', ''))
            if value_tuple not in self.correct_values:      # not allowed values
                return False

        return True

    def __convert_to_list(self, csv_data: list, has_header: bool) -> list:
        result = []

        for index in range(int(has_header), len(csv_data)):
            values = csv_data[index].split(self.separator)
            result.append([int(val) for val in values])

        return result

    def file_reader(self, has_header=True) -> str:
        """Read the file with format checking

        Raises:
            OSError: Can't read the file
            SyntaxError: File is incorrect formated

        Returns:
            str: data of file
        """

        # check access
        if not os.access(self.filename, os.R_OK):
            raise OSError("Can't read the file")

        # read
        with open(self.filename, 'r', encoding='utf-8') as file:
            raw_data = file.read()

        # check syntax
        splitted_data = raw_data.split('\n')
        if not self.__is_correct_format(splitted_data, has_header):
            raise SyntaxError('Incorect format of file')

        # convert to list of lists
        try:
            data = self.__convert_to_list(splitted_data, has_header)
            return data
        except ValueError:
            raise ValueError('File contains non-int data')

    class Calculations:
        """Nested class for calculations
        """
        def counts(self, data: list) -> tuple:
            """Count heads and tails of list of [0, 1] or [1, 0] lists
            Args:
                data (list): list for count
            Returns:
                tuple[int, int]: number of heads and tails
            """
            heads = 0
            tails = 0

            for values in data:
                if values[0]:
                    tails += 1
                else:
                    heads += 1

            return (heads, tails)

        def fractions(self, heads_and_tails: tuple) -> tuple:
            """Calculate fractions in precents
            Args:
                heads_and_tails (tuple[int, int]): number of head and tails
            Returns:
                tuple[int, int]: heads and tails fractions in precents
            """
            total = sum(heads_and_tails)
            return tuple(value / total * 100 for value in heads_and_tails)



######################
#   MAIN FUNCTION    #
######################

def main(filename: str):
    """Main function"""
    research = Research(filename)

    try:
        data = research.file_reader()
    except Exception as err:
        print(type(err).__name__, err, sep=': ')

    calculations = research.Calculations()
    counts = calculations.counts(data)
    fractions = calculations.fractions(counts)

    print(data, counts, fractions, sep='\n')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])