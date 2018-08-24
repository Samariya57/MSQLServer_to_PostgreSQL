from re import compile, VERBOSE, IGNORECASE


def sql_statements(tsql_file):
    """
    A generator that yields SQL statements from the input file one by one

    :param tsql_file: the path to the input file
    :type tsql_file: str
    """

    # These patterns are used to detect comments
    block_comment_start = compile(r'^/\*')  # The "word" starts with `/*`
    block_comment_end = compile(r'\*/')     # The "word" ends   with `*/`
    in_block_comment = False

    line_comment_start = compile(r'--')     # The "word" starts with `--`
    in_line_comment = False

    # This pattern is used to detect the beginning of SQL statements
    statement_start = \
        compile(
            r'''
                SET
               |CREATE\s+TABLE
               |ALTER\s+TABLE
               |INSERT
               |GO
            ''',
            IGNORECASE | VERBOSE
        )

    # This pattern is used to split individual lines in the file into "words"
    split_pattern = \
        compile(
            r'''
                \s+         # whitespace,
               |(?=/\*|--)  # when the following two characters are `/*` or `--',
               |(?<=\*/)    # or when the previous two characters are `*/`
            ''',
            VERBOSE         # Ignore the whitespace and text after the # in the definition string
        )

    statement = ''

    with open(tsql_file) as f:

        # Going through the file line by line
        for line in f:

            # Skipping blank lines
            if line.strip():
                m = statement_start.search(line)
                if m or (statement and statement[-2:] == ';\n'):
                    stmt = statement.strip(' \n')
                    if stmt:
                        yield stmt

                    statement = ''

                # Now, split the line into words

                words = []
                # The substring to split by
                m = split_pattern.search(line)
                while m:
                    # The start and end of the splitting substring
                    s, e = m.start(), m.end()

                    # If the split starts at 0, don't add anything to the list of words
                    if s != 0:
                        words.append(line[:s])

                    # Skip to the end of the split
                    line = line[e:]

                    # Find the next match
                    # (in case the split is by an empty substring,
                    # i.e., s == e, search from the next position)
                    m = split_pattern.search(line, pos=1 if s == e else 0)

                # If the remainder of the line is non-empty, add it to the list
                if line:
                    words.append(line)

                for word in words:
                    # First, take care of ignoring the comments
                    if in_block_comment:
                        statement += word + ' '  # Keeping the comments in

                        if block_comment_end.search(word):
                            in_block_comment = False
                        continue

                    if in_line_comment:
                        statement += word + ' '  # Keeping the comments in
                        continue

                    if block_comment_start.search(word):
                        statement += word + ' '  # Keeping the comments in

                        in_block_comment = True
                        continue

                    if line_comment_start.search(word):
                        statement += word + ' '  # Keeping the comments in

                        in_line_comment = True
                        continue

                    statement += word + ' ' if word.upper() != 'GO' else ';'

                # When we reach the end of the line, we're not in a line comment anymore
                in_line_comment = False
                statement += '\n'

    # At the end of the file, if the statement isn't empty, return it too
    stmt = statement.strip(' \n')
    if stmt:
        yield stmt


if __name__ == '__main__':
    for w in sql_statements('../initial__scripts/test.sql'):
        print(w)
        print('---------------')
