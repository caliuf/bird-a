#!/usr/bin/env python
# -*- coding: utf-8 -*-

# References:
# - Static and abstract methods: https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
# - Singletons in Python: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python?rq=1
# - Lock acquisition with a decorator: http://stackoverflow.com/questions/489720/what-are-some-common-uses-for-python-decorators/490090#490090
# - Python thread synchronization guide: http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/

import collections
import abc
import rdflib
import birda.utils.ascii_utils

NAMESPACES = {
	'rdf': rdflib.namespace.RDF,
	'rdfs': rdflib.namespace.RDFS,
	'xsd': rdflib.namespace.XSD,
	'foaf': rdflib.namespace.FOAF,
	'skos': rdflib.namespace.SKOS,
	'co': rdflib.Namespace("http://purl.org/co/"),
	'birda': rdflib.Namespace("http://w3id.org/ontologies/bird-a/"),
	'binst': rdflib.Namespace("http://pippo.it/birda-data/"),
	'tinst': rdflib.Namespace("http://pippo.it/target-data/")
}

# ============================================================================ #

class Results(object):
	"""
	Wrapper for sparql_results who provides some utility features
	"""

	query = ""
	sparql_results = []
	elapsed_time = 0.0
	
	namespaces = {}

	# ----------------------------------------------------------------------- #

	def __init__(self, query, sparql_results, elapsed_time, namespaces={}):
		self.query = query
		self.sparql_results = sparql_results
		self.elapsed_time = elapsed_time
		self.namespaces = namespaces

	# ----------------------------------------------------------------------- #
	
	def getFields(self):
		return [str(k) for k in self.sparql_results.vars]
	
	# ----------------------------------------------------------------------- #
		
	def getDictList(self):
		"""
		Get a list of dictionaries which keys are strings and values are
		RDFLib object

		:return: List of dictionaries
		"""
		
		l = []
		for res in self.sparql_results.bindings:
			l += [ dict(res) ]
		
		return l

	# ----------------------------------------------------------------------- #

	def getPrettyDictList(self):
		"""
		Get a list of dictionaries which keys are strings and values are
		pretty_urls, strings, ints and dates

		:return: List of dictionaries
		"""
		
		# Order namespaces from longest to shortest (in order to match first
		# full path instead of partial path) 
		namespaces_ordered = sorted(self.namespaces.keys(), (lambda x,y: len(x)-len(y)), reverse=True )
		
		l = []
		for res in self.sparql_results.bindings:
			d = {}
			for k in self.getFields():
				if type(res[k]) == type(rdflib.term.URIRef('')):
					uri = str(res[k])
					
					# Namespaces substitution
					for ns in namespaces_ordered:
						if uri.startswith(str(self.namespaces[ns])):
							uri = uri.replace(str(self.namespaces[ns]), ns+':')
							break
					
					d[str(k)] = '<'+uri+'>'
				
				else:
					if res[k].datatype:
						datatype = str(res[k].datatype).split('#')[-1]
						d[str(k)] = "%s^^%s" % (res[k].value, datatype)
					else:
						if res[k].language:
							d[str(k)] = '"%s"@%s' % (res[k].value, res[k].language)
						else:
							d[str(k)] = '"%s"' % (res[k].value)
				
			l += [ d ]
		
		return l

	# ----------------------------------------------------------------------- #

	def printQueryResults(self):
		"""
		Print query results in a MySQL ascii tab fashion

		:return: None
		"""
		
		print '===================================='
		print self.query.replace('\t','  ')
		print '===================================='
		print birda.utils.ascii_utils.render_list_dict( self.getPrettyDictList(), map=self.getFields() ) ,
		print "%s rows in set (%s sec)" % ( len(self.getPrettyDictList()), birda.utils.ascii_utils.hhmmss(self.elapsed_time,tutto=False) )
		print
		
# ============================================================================ #

class Connection(object):
	__metaclass__  = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self, settings, dataset='', namespaces={}):
		pass

	@abc.abstractmethod
	def query(self, query):
		"""
		Exectutes a read-only sparql query

		:return: Result object
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	@abc.abstractmethod
	def update(self, query):
		"""
		Exectutes a write-only sparql query

		:return: ???
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	@abc.abstractmethod
	def close(self):
		"""
		Close the connection

		:return: None
		"""
		raise NotImplementedError("This method should be implemented by subclasses")

# ============================================================================ #

class Storage(object):
	"""
	Storage abstract class

	"""

	# ----------------------------------------------------------------------- #

	def __init__(self):
		raise NotImplementedError("Storage should not be instantiated")

	# ----------------------------------------------------------------------- #

	@staticmethod
	def connect(settings, dataset='', namespaces=NAMESPACES):
		"""
		Creates a connection to a sparql endpoint using "setting" parameters

		:return: Connection object (sublass of storage.Connection)
		"""

		if settings['birda_storage_type'] == 'file':
			import file_storage
			return file_storage.FileConnection(settings, dataset=dataset, namespaces=namespaces)
		else:
			raise NotImplementedError("Storage type unknown")

# ================================================================================================ #

if __name__ == '__main__':
	storage = Storage()