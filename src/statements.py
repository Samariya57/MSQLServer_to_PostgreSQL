from re import compile, VERBOSE, IGNORECASE

# This pattern is used to detect the beginning of SQL statements
statement_start = \
    compile(
        r'''
            ^\s*(?:           # Looking at the beginning of the string (except skipping any whitespace)
            SET               # for any of these keywords
           |CREATE\s+TABLE
           |ALTER\s+TABLE
           |INSERT
           |GO
           )\b                # Making sure a word ends here (so, for instance, `GOES` won't match)
        ''',
        IGNORECASE | VERBOSE  # ignoring case, whitespace, and comments
    )


def sql_statements(tsql_file):
    """
    A generator that yields SQL statements from the input file one by one

    **Example:**
        ``for stmt in sql_statements('<path>/<filename>.sql'):``
            ``print(stmt)``

    :param tsql_file: the path to the input file
    :type tsql_file: str
    """
    global statement_start

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
                    yield 'GO'
                else:
                    statement += line

    # At the end of the file, if the statement isn't empty, return it too
    stmt = statement.strip()
    if stmt:
        if stmt == 'GO':
            yield 'GO'
        else:
            yield statement.strip('\n')
