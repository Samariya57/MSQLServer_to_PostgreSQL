from re import compile, VERBOSE, IGNORECASE


def sql_statements(tsql_file):
    """
    A generator that yields SQL statements from the input file one by one

    :param tsql_file: the path to the input file
    :type tsql_file: str
    """

    # This pattern is used to detect the beginning of SQL statements
    statement_start = \
        compile(
            r'''
                ^\s*(?:
                SET
               |CREATE\s+TABLE
               |ALTER\s+TABLE
               |INSERT
               |GO)\b
            ''',
            IGNORECASE | VERBOSE
        )

    statement = ''
    with open(tsql_file) as f:
        # Going through the file line by line
        for line in f:
            if line.strip():  # Skipping blank lines

                m = statement_start.search(line)
                if m:
                    stmt = statement.strip()
                    if stmt:
                        yield statement.strip('\n')

                    statement = ''

                if line.strip() == 'GO':
                    yield ';'
                else:
                    statement += line

    # At the end of the file, if the statement isn't empty, return it too
    stmt = statement.strip()
    if stmt:
        if stmt == 'GO':
            yield ';'
        else:
            yield statement.strip('\n')


# A small test
if __name__ == '__main__':
    for w in sql_statements('../initial__scripts/test.sql'):
        print(w)
        print('------- end of statement -------')
