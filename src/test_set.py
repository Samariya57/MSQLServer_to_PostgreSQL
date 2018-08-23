#
# To run the tests,
# first install pytest: `pip install pytest`,
# then run py.test from the directory containing this file
#

import set


def test_set():
    assert set.set_psql('set NOCOUNT ON') == '-- (from T-SQL) SET NOCOUNT ON;'
    assert set.set_psql('SET NOCOUNT OFF') == '-- (from T-SQL) SET NOCOUNT OFF;'
    assert set.set_psql('SET ansi_NULLS ON') == '-- (from T-SQL) SET ansi_NULLS ON;'
    assert set.set_psql('set ANSI_NULLS OFF') == '-- (from T-SQL) SET ANSI_NULLS OFF;'
    assert set.set_psql('SET QUOTED_IDENTIFIER ON') == '-- (from T-SQL) SET QUOTED_IDENTIFIER ON;'
    assert set.set_psql('SET QUOTED_IDENTIFIER OFF') == '-- (from T-SQL) SET QUOTED_IDENTIFIER OFF;'

    assert \
        set.set_psql(
            'SET IDENTITY_INSERT [table] OFF'
        ) == \
        '-- (from T-SQL) SET IDENTITY_INSERT [table] OFF;'
    assert \
        set.set_psql(
            'SET IDENTITY_INSERT [schema].[table] OFF'
        ) == \
        '-- (from T-SQL) SET IDENTITY_INSERT [schema].[table] OFF;'
    assert \
        set.set_psql(
            'SET IDENTITY_INSERT [db].[schema].[table] OFF'
        ) == \
        '-- (from T-SQL) SET IDENTITY_INSERT [db].[schema].[table] OFF;'

    assert \
        set.set_psql(
            'SET iDeNtITY_INSERT [table] ON'
        ) == \
        '-- Add the following after explicitly inserting values into the serial column of "table"\n' + \
        '-- (replacing <id_column_name> with the name of the serial column):\n' + \
        '-- SELECT setval(\n' + \
        '--    pg_get_serial_sequence("table", <id_column_name>),\n' + \
        '--    (SELECT MAX(<id_column_name>) FROM "table"\n' + \
        '-- );'
    assert \
        set.set_psql(
            'SET IDENTITY_INSERT [schema].[table] ON'
        ) == \
        '-- Add the following after explicitly inserting values into the serial column of "schema"."table"\n' + \
        '-- (replacing <id_column_name> with the name of the serial column):\n' + \
        '-- SELECT setval(\n' + \
        '--    pg_get_serial_sequence("schema"."table", <id_column_name>),\n' + \
        '--    (SELECT MAX(<id_column_name>) FROM "schema"."table"\n' + \
        '-- );'
    assert \
        set.set_psql(
            'SET IDENTITY_INSERT [db].[schema].[table] ON'
        ) == \
        '-- Add the following after explicitly inserting values into the serial column of "db"."schema"."table"\n' + \
        '-- (replacing <id_column_name> with the name of the serial column):\n' + \
        '-- SELECT setval(\n' + \
        '--    pg_get_serial_sequence("db"."schema"."table", <id_column_name>),\n' + \
        '--    (SELECT MAX(<id_column_name>) FROM "db"."schema"."table"\n' + \
        '-- );'
