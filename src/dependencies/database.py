


from src.database.connect import sessionLocal


def get_db():
	db = sessionLocal()
	try:
		yield db
	except Exception:
		db.rollback()
		raise
	finally:
		db.close()

