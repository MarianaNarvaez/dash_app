CONN: str = """Driver={SQL Server};Server='';Database='';Trusted_Connection=yes;"""

PASSWORD = '*******'

QUERY_MFG_HANA = """
""".replace('\n','')

QUERY_HELDWARE_HANA = """
""".replace('\n','')

QUERY_SEVERITY_HANA = """
SELECT...
""".replace('\n','')

QUERY_GEOGRAPHY = """
select * from ...
""".replace('\n','')

INSERT_STATEMENT_MFG = """
INSERT INTO...
)""".replace('\n','')

UPDATE_STATEMENT_MFG = """
UPDATE...
""".replace('\n','')

INSERT_STATEMENT_EHS = """
INSERT INTO...
""".replace('\n','')

UPDATE_STATEMENT_EHS = """
UPDATE ...
""".replace('\n','')

INSERT_STATEMENT_MANUFACTURING = """
INSERT INTO...
""".replace('\n','')

UPDATE_STATEMENT_MANUFACTURING = """
UPDATE...
""".replace('\n','')


INSERT_STATEMENT_QUALITY = """
INSERT INTO...
""".replace('\n','')


UPDATE_STATEMENT_QUALITY = """
UPDATE...
""".replace('\n','')


QUERY_ALL_PLANTS_WEEK = """
SELECT...
""".replace('\n','')

QUERY_MFG_PLANT = """
SELECT...
""".replace('\n','')

QUERY_MFG_MANUFACTURING = """
SELECT...
""".replace('\n','')

QUERY_EHS = """
SELECT...
""".replace('\n','')

QUERY_QUALITY = """
SELECT...
""".replace('\n','')

DELETE_STATEMENT_EHS = """
DELETE FROM ...
""".replace('\n','')

DELETE_STATEMENT_MFG = """
DELETE FROM ...
""".replace('\n','')

DELETE_STATEMENT_PLANTS = """
DELETE FROM ...
""".replace('\n','')

DELETE_STATEMENT_QUA = """
DELETE FROM ...
""".replace('\n','')

VALID_USERNAME_PASSWORD_PAIRS = {
    '' : '',
    '' : '',
    '' : '',
    '' : '',
    '' : ''
}