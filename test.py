def myfunc(readonly=True, metadata=False, special=None):
	''' scripts or photos or appdata or file passed in as True overrides everything else, in terms of scope.  Error if both are true.'''
	link_root = linkjoin(AUTH_LINK_ROOT, 'drive')
	'''
	if len([x for x in (file, photos, scripts, appdata) if x]) > 1:
		raise ValueError("Can't set more than one of photos, scripts, file and appdata as true.  Any one of these set to true override all other arguments")
	'''
	if special is not None:
		if special == 'file':
			self.scope = dotjoin(link_root, 'file')
			return
		elif special == 'photos':
			self.scope = dotjoin(link_root, 'photos', 'readonly')
			return
		elif special == 'scripts':
			self.scope = dotjoin(link_root, 'scripts')
			return
		elif special == 'appdata':
			self.scope = dotjoin(link_root, 'appdata')
			return
		else:
			raise ValueError('special argument must be either None (default) or one of {}.'.format(self.SPECIAL_OPTIONS))
	else:
		scope = link_root
		if metadata:
			scope = dotjoin(scope, 'metadata')
		if readonly:
			scope = dotjoin(scope, 'readonly')

		self.scope = scope