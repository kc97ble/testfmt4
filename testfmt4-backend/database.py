import sqlalchemy as sa

# TODO: change db location
engine = sa.create_engine("sqlite:////tmp/test.db")
metaData = sa.MetaData(engine)

uploads_table = sa.Table(
    "uploads",
    metaData,
    sa.Column("file_id", sa.String(255), primary_key=True),
    sa.Column("file_name", sa.String(255)),
)

metaData.create_all()


def drop_db():
    for table in reversed(metaData.sorted_tables):
        table.drop(engine)


def add_upload_info(file_id, file_name):
    #  pylint: disable=no-value-for-parameter
    stmt = uploads_table.insert().values(file_id=file_id, file_name=file_name)
    conn = engine.connect()
    return conn.execute(stmt)


def get_upload_info(file_id):
    stmt = sa.select([uploads_table]).where(uploads_table.c.file_id == file_id)
    conn = engine.connect()
    rows = conn.execute(stmt)
    return dict(rows.fetchone())
