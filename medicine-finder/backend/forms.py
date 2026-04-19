def get_form_value(form, key, default=""):
	return (form.get(key, default) or "").strip()


def get_form_int(form, key, default=0):
	try:
		return int((form.get(key, "") or "").strip())
	except ValueError:
		return default
